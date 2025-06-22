from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from
from models import db, User, Roll
import os
import datetime
import logging
from flask import request

app = Flask(__name__)
BASEDIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(BASEDIR, 'assets', 'rolls.db')}"
swagger = Swagger(app)
db.init_app(app)

logging.basicConfig(level=logging.INFO)


@app.before_request
def log_request_info():
    logging.info(f"Request: {request.method} {request.url}")
    logging.info(f"Headers: {dict(request.headers)}")
    logging.info(f"Body: {request.get_data().decode('utf-8')}")


@app.route('/roll', methods=["POST"])
def roll():
    """
    Record a new dice roll linked to a user by pixelId.
    ---
    tags:
      - Rolls
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - pixelId
              - faceValue
            properties:
              pixelId:
                type: string
                description: Unique pixel identifier for the user
                example: "abc123"
              faceValue:
                type: integer
                description: The rolled face value of the d20
                example: 15
    responses:
      201:
        description: Roll recorded successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Roll recorded"
                roll:
                  type: object
                  properties:
                    id:
                      type: integer
                      example: 1
                    value:
                      type: integer
                      example: 15
                    timestamp:
                      type: string
                      format: date-time
                      example: "2025-05-26T14:34:00Z"
                    user_id:
                      type: integer
                      example: 42
                    pixelId:
                      type: string
                      example: "abc123"
      400:
        description: Missing or invalid parameters
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Missing 'pixelId' or 'faceValue' in request"
      404:
        description: User not found
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "User with pixelId 'abc123' not found"
    """
    data = request.get_json()

    pixel_id = data.get('pixelId')
    value = data.get('faceValue')

    print(pixel_id)

    if not pixel_id or value is None:
        return jsonify({"error": "Missing 'pixelId' or 'faceValue' in request"}), 400

    user = User.query.filter_by(pixelId=pixel_id).first()
    if not user:
        return jsonify({"error": f"User with pixelId '{pixel_id}' not found"}), 404

    new_roll = Roll(
        value=value,
        user_id=user.id,
        timestamp=datetime.datetime.utcnow()
    )

    db.session.add(new_roll)
    db.session.commit()

    return jsonify({
        "message": "Roll recorded",
        "roll": {
            "id": new_roll.id,
            "value": new_roll.value,
            "timestamp": new_roll.timestamp.isoformat() + "Z",
            "user_id": new_roll.user_id,
            "pixelId": pixel_id
        }
    }), 201

@app.route('/api/users', methods=['POST'])
def add_user():
    """
    Create a new user.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - pixelId
            - username
          properties:
            pixelId:
              type: string
              description: Unique ID from the pixel device.
              example: abc123
            username:
              type: string
              description: Display name of the user.
              example: wizardroller
    responses:
      201:
        description: User successfully created.
        schema:
          type: object
          properties:
            id:
              type: integer
            pixelId:
              type: string
            username:
              type: string
      400:
        description: Missing required fields.
        schema:
          type: object
          properties:
            error:
              type: string
    """
    data = request.get_json()

    if not data or 'pixelId' not in data or 'username' not in data:
        return jsonify({'error': 'Missing pixelId or username'}), 400

    new_user = User(
        pixelId=data['pixelId'],
        username=data['username']
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        'id': new_user.id,
        'pixelId': new_user.pixelId,
        'username': new_user.username
    }), 201

@app.route('/rolls/', defaults={'n': 10}, methods=['GET'])
@swag_from({
    'summary': 'Get the last N rolls with joined user info',
    'description': 'Returns the latest N rolls from the database using an explicit join. Includes user data.',
    'parameters': [
        {
            'name': 'n',
            'in': 'path',
            'type': 'integer',
            'required': False,
            'description': 'Number of latest rolls to retrieve. Defaults to 10.',
            'default': 10
        }
    ],
    'responses': {
        200: {
            'description': 'List of roll results with user data (joined)',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'value': {'type': 'integer'},
                        'timestamp': {'type': 'string', 'format': 'date-time'},
                        'user': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer'},
                                'pixelId': {'type': 'string'},
                                'username': {'type': 'string'}
                            }
                        }
                    }
                }
            }
        }
    }
})
def get_last_rolls(n):
    # Using explicit join
    results = (
        db.session.query(Roll, User)
        .join(User, Roll.user_id == User.id)
        .order_by(Roll.timestamp.desc())
        .limit(n)
        .all()
    )

    return jsonify([
        {
            'id': roll.id,
            'value': roll.value,
            'timestamp': roll.timestamp.isoformat(),
            'user': {
                'id': user.id,
                'pixelId': user.pixelId,
                'username': user.username
            }
        }
        for roll, user in results
    ])





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

