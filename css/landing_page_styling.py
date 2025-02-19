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
      <img src="https://drive.google.com/uc?export=view&id=1UU0qRJ7i2P8tc01Gqv3GNiS4_-4GpfS9" alt="Vesta Logo" class="logo">
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
