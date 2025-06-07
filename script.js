function cancelPendingReservations() {
  const now = new Date();
  const today7pm = new Date();
  today7pm.setHours(19, 0, 0, 0); // 7 PM today

  if (now >= today7pm) {
    let reservations = JSON.parse(localStorage.getItem('reservations') || "[]");
    let changed = false;

    reservations = reservations.map(r => {
      if (r.status === "pending" && !r.cardNumber) {
        r.status = "cancelled";
        changed = true;
      }
      return r;
    });

    if (changed) {
      localStorage.setItem('reservations', JSON.stringify(reservations));
      console.log("Pending reservations without credit cards cancelled.");
    }
  }
}


// Run once when page loads
cancelPendingReservations();

// app.js or server.js
const express = require('express');
const app = express();
const path = require('path');

app.use(express.static('public')); // Folder where dashboard.html is stored

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'admin-login.html'));
});

app.listen(3000, () => {
  console.log('Server started at http://localhost:3000');
});
