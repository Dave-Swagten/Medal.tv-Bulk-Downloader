# 🎥 Medal.tv Bulk Downloader

**Medal.tv Bulk Downloader** is a simple and powerful Python tool designed to help you download all your video clips from Medal.tv in bulk. Whether you're looking to back up your memories or organize your content, this tool makes it easy!

---

## 📖 My Story

I've been using Medal.tv since 2019. Over the years, I've accumulated thousands of clips that I wanted to save locally. I kept asking Medal for a feature that would let me download all my clips (or lots of them) at once, but unfortunately, it never came.

After waiting for so long, I decided to take matters into my own hands and build this tool. It's my way of ensuring that all my memories are safe and sound on my own terms. And now, I'm sharing it with the community in the hope that it helps others like me!

---

## ✨ Features

- **Bulk Download**: Fetch and download all your clips as `.mp4` files in one go.
- **Automatic Naming**: Files are named based on the upload date and title, so your clips stay organized.
- **Batch Processing**: Handles large numbers of clips by processing them in manageable batches.

---

## 🛠️ Getting Started

### 1. Clone the Repository

Start by cloning the repository to your local machine:

```bash
git clone https://github.com/Dave-Swagten/Medal.tv-Bulk-Downloader.git
cd Medal.tv-Bulk-Downloader/src
```

---

## ⚙️ Configuration

Before you can start downloading your clips, you'll need to set up the `config.json` file with your Medal.tv username and cookies.

### 1. Rename the Configuration File

Rename the example configuration file:

```bash
mv example.config.json config.json
```

### 2. Set up your username and Cookies

#### 🆔 Configuring your username

Open `config.json` in a text editor and simply add your username like this:

```json
{
  "username": "your_medal_username"
}
```

#### 🍪 Exporting Your Cookies

To get your cookies:

1. Install a browser add-on like [Cookie-Editor](https://cookie-editor.com/).
2. Go to [Medal.tv](https://medal.tv/) and make sure you are logged in.
3. Open the Cookie-Editor and export your cookies in JSON format.

### 3. Update `config.json`

Once you have your username and cookies, open `config.json` in a text editor and update it like the example:

```json
{
  "username": "user123",
  "cookies": [
    {
      "domain": ".medal.tv",
      "expirationDate": 1695555555,
      "hostOnly": false,
      "httpOnly": true,
      "name": "cookie_name",
      "path": "/",
      "sameSite": "Lax",
      "secure": true,
      "session": false,
      "storeId": null,
      "value": "cookie_value",
      "id": 1
    }
    // More cookies here, make sure to include all the exported cookies provided by your browser.
  ]
}
```

---

## 🚀 How to Use

Once everything is set up, you're ready to start downloading your clips!

### Run the Script

To start downloading your Medal.tv videos, run:

```bash
python main.py
```

The script will fetch your videos and save them to the `downloads` folder. Files are named based on their upload date and title to keep things organized.

---

## 💡 Tips & Tricks

- **Edit the Script**: Feel free to tweak the script to better suit your needs or contribute to its development!

---

## 🔧 Troubleshooting

- **Cookie Issues?**: Ensure that your cookies are in the correct JSON format and include all necessary data as exported by the browser.

---

## 📜 License

This project is licensed under the MIT License. For more details, see the [LICENSE](LICENSE) file.

---

## 💻 Requirements

- Python 3.10 (used in development)
- No additional packages required ;P

---

## ❤️ Contributing

If you have ideas for improvements or want to help with development, feel free to fork this repository and submit a pull request. Your contributions are welcome :D
