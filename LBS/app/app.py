from flask import Flask, render_template, jsonify
from models import db, Meter, MeterData

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/health')
def health_check():
    return jsonify(status='ok')


@app.route('/meters/', methods=['GET'])
def get_meters():
    meters: Meter = Meter.query.all()
    if not meters:
        return render_template('meters.html', meters=[]), 404
    return render_template('meters.html', meters=meters), 200


@app.route('/meters/<int:meter_id>/', methods=['GET'])
def get_meter_data(meter_id):
    data: MeterData = MeterData.query.filter_by(
                                    meter_id=meter_id
                                    ).order_by(
                                        MeterData.timestamp
                                        ).all()
    if not data:
        return jsonify(
                        {'error': f'No data found for meter ID {meter_id}'
                         }
                            ), 404
    return jsonify(
                    [
                        {
                            'id': entry.id,
                            'meter_id': entry.meter_id,
                            'timestamp': entry.timestamp,
                            'value': entry.value
                            } for entry in data
                        ]
                    ), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0')
