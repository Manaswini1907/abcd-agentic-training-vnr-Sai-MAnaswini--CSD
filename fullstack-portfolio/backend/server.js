const express = require("express");
const cors = require("cors");
const fs = require("fs");

const app = express();

app.use(cors());
app.use(express.json());

// Route to save contact form data
app.post("/contact", (req, res) => {

    const newMessage = req.body;

    // Read existing data
    let messages = [];

    if (fs.existsSync("messages.json")) {
        const data = fs.readFileSync("messages.json");
        messages = JSON.parse(data);
    }

    // Add new message
    messages.push(newMessage);

    // Save back to file
    fs.writeFileSync("messages.json", JSON.stringify(messages, null, 2));

    res.json({ message: "Message Saved Successfully!" });
});

app.listen(5000, () => {
    console.log("Server running on port 5000");
});
