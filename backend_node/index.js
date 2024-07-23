// In your Express server file
const express = require("express");
const cors = require('cors');
const qrcode = require('qrcode');
const port = 8001;

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({extended: true}));

app.post('/get-qr-code', (req, res) => {
    const otp_auth_url = req.body.otp_auth_url;
    qrcode.toDataURL(otp_auth_url, function(err, data) {
        if (err) {
            return res.status(500).json({ error: 'Failed to generate QR code' });
        }
        return res.status(200).json({ qr_code_link: data });
    });
});

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});
