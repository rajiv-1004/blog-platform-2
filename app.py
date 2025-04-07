from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# In-memory posts list
posts = []
post_id_counter = 1

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/posts/', methods=['GET'])
def get_posts():
    return jsonify(posts)

@app.route('/api/posts/', methods=['POST'])
def create_post():
    global post_id_counter
    data = request.get_json()
    data['id'] = post_id_counter
    posts.append(data)
    post_id_counter += 1
    return jsonify(data), 201

@app.route('/api/posts/<int:post_id>/', methods=['DELETE'])
def delete_post(post_id):
    global posts
    posts = [post for post in posts if post['id'] != post_id]
    return '', 204

@app.route('/api/posts/<int:post_id>/', methods=['PUT'])
def update_post(post_id):
    data = request.get_json()
    for post in posts:
        if post['id'] == post_id:
            post['title'] = data['title']
            post['content'] = data['content']
            return jsonify(post)
    return jsonify({'error': 'Post not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
