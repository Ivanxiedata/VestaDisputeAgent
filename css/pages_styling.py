
smart_contract_page_style = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Smart Contract Agent Started</title>
    <link
      href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap"
      rel="stylesheet"
    />
    <style>
      body {
        margin: 0;
        padding: 0;
        font-family: 'Roboto', sans-serif;
        background: linear-gradient(135deg, #667eea, #764ba2);
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        color: #ffffff;
      }

      .container {
        background-color: rgba(0, 0, 0, 0.4);
        padding: 2rem 3rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
      }

      h1 {
        margin-bottom: 1rem;
        font-size: 2rem;
      }

      p {
        margin-bottom: 1rem;
        font-size: 1.1rem;
      }

      a {
        text-decoration: none;
        color: #ffd700;
        font-weight: 700;
        transition: color 0.3s ease, transform 0.3s ease;
      }

      a:hover {
        color: #ffea00;
        transform: scale(1.05);
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>Smart Contract Agent Started</h1>
      <p>The Smart Contract Agent has been started on port <strong>8002</strong>.</p>
      <p>
        Please check your Chainlit chat interface at
        <a href="http://127.0.0.1:8002" target="_blank" rel="noopener noreferrer">
          http://127.0.0.1:8002
        </a>
        for further instructions.
      </p>
      <p>
        <a href="/">Back to Home</a>
      </p>
    </div>
  </body>
</html>

"""
dispute_page_style = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Dispute Agent Started</title>
    <link
      href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap"
      rel="stylesheet"
    />
    <style>
      body {
        margin: 0;
        padding: 0;
        font-family: 'Roboto', sans-serif;
        background: linear-gradient(135deg, #ff7e5f, #feb47b);
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        color: #ffffff;
      }

      .container {
        background-color: rgba(0, 0, 0, 0.4);
        padding: 2rem 3rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
      }

      h1 {
        margin-bottom: 1rem;
        font-size: 2rem;
      }

      p {
        margin-bottom: 1rem;
        font-size: 1.1rem;
      }

      a {
        text-decoration: none;
        color: #ffd700;
        font-weight: 700;
        transition: color 0.3s ease, transform 0.3s ease;
      }

      a:hover {
        color: #ffea00;
        transform: scale(1.05);
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>Dispute Agent Started</h1>
      <p>The Dispute Agent has been started on port <strong>8000</strong>.</p>
      <p>
        Please check your Chainlit chat interface at
        <a href="http://127.0.0.1:8003" target="_blank" rel="noopener noreferrer">
          http://127.0.0.1:8003
        </a>
        for further instructions.
      </p>
      <p>
        <a href="/">Back to Home</a>
      </p>
    </div>
  </body>
</html>

"""

landing_page_style = """
<!DOCTYPE html>
<html>
  <head>
    <title>Vesta Platform</title>
    <style>
      body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        margin: 0;
        padding: 0;
        background: #f7f7f7;
        color: #333;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
      }
      .container {
        background: #fff;
        padding: 40px;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        text-align: center;
        max-width: 500px;
        width: 90%;
      }
      .logo {
        width: 120px;
        margin-bottom: 20px;
      }
      h1 {
        margin: 10px 0;
        font-size: 2em;
      }
      p {
        font-size: 1.1em;
        margin-bottom: 30px;
      }
      .btn {
        font-size: 1em;
        padding: 12px 25px;
        margin: 10px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        transition: background 0.3s ease;
      }
      .btn-primary {
        background: #007bff;
        color: #fff;
      }
      .btn-primary:hover {
        background: #0056b3;
      }
      .btn-secondary {
        background: #6c757d;
        color: #fff;
      }
      .btn-secondary:hover {
        background: #565e64;
      }
      a {
        text-decoration: none;
        color: inherit;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <!-- Using the direct Google Drive URL -->
      <img src="https://drive.google.com/file/d/1UU0qRJ7i2P8tc01Gqv3GNiS4_-4GpfS9/view?usp=sharing" alt="Vesta Logo" class="logo">
      <h1>Welcome to Vesta</h1>
      <p>Your trusted platform for smart contracts and dispute resolution.</p>
      <button class="btn btn-primary" onclick="window.location.href='/smart_contract'">
        Create Smart Contract
      </button>
      <button class="btn btn-secondary" onclick="window.location.href='/dispute'">
        Enter Dispute
      </button>
    </div>
  </body>
</html>
"""
