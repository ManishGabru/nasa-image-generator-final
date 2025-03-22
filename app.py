from flask import Flask, jsonify, request, send_from_directory
import requests, random
from flask_cors import CORS

app = Flask(__name__, static_folder="static")
CORS(app)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/get_image')
def get_image():
    try:
        query = request.args.get('query', 'deep space')
        page = int(request.args.get('page', 1))
        resp = requests.get(f"https://images-api.nasa.gov/search?media_type=image&q={query}&page={page}")
        items = resp.json().get('collection', {}).get('items', [])

        space_keywords = ['nebula', 'galaxy', 'supernova', 'star', 'deep space', 'cosmos', 'universe', 'black hole', 'cluster']
        filtered = [item for item in items if any(keyword in item['data'][0]['title'].lower() for keyword in space_keywords)]

        if not filtered:
            return jsonify({"error": "No deep space images found on page " + str(page)})

        item = random.choice(filtered)
        metadata = item['data'][0]
        image_url = item['links'][0]['href']

        return jsonify({
            "image_url": image_url,
            "telescope": metadata.get('secondary_creator', 'NASA Telescope'),
            "observation_date": metadata.get('date_created'),
            "object_name": metadata.get('title'),
            "description": metadata.get('description')
        })
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
