# app.py
import os, json
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify
from config import FLASK_SECRET_KEY
from models import db, WeatherRecord
from weather_api import geocode, get_current_weather, get_forecast
from utils import validate_dates
from exports import export_to_csv, export_to_json, export_to_pdf
from datetime import datetime
from io import BytesIO

app = Flask(__name__)
app.config["SECRET_KEY"] = FLASK_SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        location = request.form.get("location", "").strip()
        if not location:
            flash("Enter a location", "warning"); return redirect(url_for("index"))
        ge = geocode(location)
        if not ge:
            flash("Could not resolve location", "danger"); return redirect(url_for("index"))
        try:
            current = get_current_weather(ge["lat"], ge["lon"])
            forecast = get_forecast(ge["lat"], ge["lon"])
        except Exception as e:
            flash(f"API error: {e}", "danger"); return redirect(url_for("index"))
        return render_template("results.html", place=ge["name"], lat=ge["lat"], lon=ge["lon"], weather=current, forecast=forecast)
    return render_template("index.html")

@app.route("/save_record", methods=["POST"])
def save_record():
    location_text = request.form.get("location_text","").strip()
    lat = request.form.get("lat"); lon = request.form.get("lon")
    start_date = request.form.get("start_date"); end_date = request.form.get("end_date")
    ok, res = validate_dates(start_date, end_date) if start_date and end_date else (False, "Provide date range")
    if not ok:
        flash(res, "danger"); return redirect(url_for("index"))
    if not lat or not lon:
        ge = geocode(location_text)
        if not ge: flash("Could not geocode", "danger"); return redirect(url_for("index"))
        lat = ge["lat"]; lon = ge["lon"]; location_text = ge["name"]
    try:
        current = get_current_weather(lat, lon); forecast = get_forecast(lat, lon)
    except Exception as e:
        flash(f"API error: {e}", "danger"); return redirect(url_for("index"))
    payload = {"fetched_at": datetime.utcnow().isoformat(), "query": {"start_date": start_date, "end_date": end_date}, "current": current, "forecast": forecast}
    rec = WeatherRecord(location_text=location_text, lat=float(lat), lon=float(lon), start_date=start_date, end_date=end_date, payload_json=json.dumps(payload))
    db.session.add(rec); db.session.commit()
    flash("Record saved", "success"); return redirect(url_for("records"))

@app.route("/records")
def records():
    recs = WeatherRecord.query.order_by(WeatherRecord.created_at.desc()).all()
    return render_template("records.html", records=recs)

@app.route("/record/<int:rec_id>")
def view_record(rec_id):
    rec = WeatherRecord.query.get_or_404(rec_id)
    data = json.loads(rec.payload_json)
    return render_template("view_record.html", rec=rec, data=data)

@app.route("/record/<int:rec_id>/edit", methods=["GET","POST"])
def update_record(rec_id):
    rec = WeatherRecord.query.get_or_404(rec_id)
    if request.method == "POST":
        location_text = request.form.get("location_text","").strip()
        start_date = request.form.get("start_date"); end_date = request.form.get("end_date")
        ok, res = validate_dates(start_date, end_date)
        if not ok:
            flash(res, "danger"); return redirect(url_for("update_record", rec_id=rec_id))
        if location_text != rec.location_text:
            ge = geocode(location_text)
            if not ge: flash("Cannot geocode new location", "danger"); return redirect(url_for("update_record", rec_id=rec_id))
            rec.location_text = ge["name"]; rec.lat = ge["lat"]; rec.lon = ge["lon"]
            try:
                current = get_current_weather(rec.lat, rec.lon); forecast = get_forecast(rec.lat, rec.lon)
            except Exception as e:
                flash(f"API error: {e}", "danger"); return redirect(url_for("update_record", rec_id=rec_id))
            rec.payload_json = json.dumps({"fetched_at": datetime.utcnow().isoformat(), "query": {"start_date": start_date, "end_date": end_date}, "current": current, "forecast": forecast})
        rec.start_date = start_date; rec.end_date = end_date
        db.session.commit(); flash("Updated", "success"); return redirect(url_for("records"))
    return render_template("update_record.html", rec=rec)

@app.route("/record/<int:rec_id>/delete", methods=["POST"])
def delete_record(rec_id):
    rec = WeatherRecord.query.get_or_404(rec_id)
    db.session.delete(rec); db.session.commit(); flash("Deleted", "success"); return redirect(url_for("records"))

@app.route("/export/<fmt>")
def export_all(fmt):
    recs = WeatherRecord.query.all()
    rows = []
    for r in recs:
        d = r.to_dict()
        rows.append({"id": d["id"], "created_at": d["created_at"], "location": d["location_text"], "start_date": d["start_date"], "end_date": d["end_date"], "sample": d["payload"].get("current", {}).get("weather", [{}])[0].get("description","")})
    os.makedirs("exports", exist_ok=True)
    if fmt == "csv":
        path = os.path.join("exports","records.csv"); export_to_csv(rows, path); return send_file(path, as_attachment=True)
    elif fmt == "json":
        path = os.path.join("exports","records.json"); export_to_json(rows, path); return send_file(path, as_attachment=True)
    elif fmt == "pdf":
        b = export_to_pdf(rows); return send_file(BytesIO(b), mimetype="application/pdf", download_name="records.pdf", as_attachment=True)
    else:
        flash("Unsupported", "warning"); return redirect(url_for("records"))

@app.route("/external_links/<int:rec_id>")
def external_links(rec_id):
    rec = WeatherRecord.query.get_or_404(rec_id)
    maps = f"https://www.google.com/maps/search/?api=1&query={rec.lat},{rec.lon}"
    yt = f"https://www.youtube.com/results?search_query={requests.utils.quote(rec.location_text + ' travel')}"
    return jsonify({"maps": maps, "youtube": yt})

if __name__ == "__main__":
    app.run(debug=True)