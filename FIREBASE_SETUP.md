# Firebase Authentication Setup Guide

This guide will help you set up Firebase Authentication for your leaked database security service.

## Why Firebase?

- **Real server-side authentication** - Credentials never stored in client code
- **Secure** - Password hashes managed by Google's infrastructure
- **Free tier** - 10K verifications/month (plenty for personal use)
- **Easy management** - Add/remove users via Firebase Console
- **No backend needed** - Works with static GitHub Pages

## Step 1: Create Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click **"Add project"** or **"Create a project"**
3. Enter project name: `leaked-db-auth` (or your choice)
4. Disable Google Analytics (not needed for this project)
5. Click **"Create project"**

## Step 2: Enable Email/Password Authentication

1. In your Firebase project, click **"Authentication"** in the left sidebar
2. Click **"Get started"**
3. Click the **"Sign-in method"** tab
4. Click **"Email/Password"**
5. Toggle **"Enable"** to ON
6. Click **"Save"**

## Step 3: Add Your First User

1. Still in Authentication, click the **"Users"** tab
2. Click **"Add user"**
3. Enter your email (e.g., `admin@yourdomain.com`)
4. Enter a strong password
5. Click **"Add user"**

**Important:** This email/password combination is what you'll use to access your leaked database site.

## Step 4: Get Firebase Configuration

1. In Firebase Console, click the gear icon ⚙️ next to "Project Overview"
2. Click **"Project settings"**
3. Scroll down to **"Your apps"**
4. Click the **Web** icon `</>`
5. Register app with nickname: `leak-db-web`
6. **DO NOT** check "Also set up Firebase Hosting"
7. Click **"Register app"**
8. Copy the `firebaseConfig` object

You'll see something like:

```javascript
const firebaseConfig = {
  apiKey: "AIzaSyC...",
  authDomain: "leaked-db-auth.firebaseapp.com",
  projectId: "leaked-db-auth",
  storageBucket: "leaked-db-auth.appspot.com",
  messagingSenderId: "123456789",
  appId: "1:123456789:web:abc123"
};
```

## Step 5: Update index.html

1. Open `index.html` in your code
2. Find the `firebaseConfig` object (around line 8-16)
3. Replace the placeholder values with your actual Firebase config:

```javascript
const firebaseConfig = {
    apiKey: "YOUR_ACTUAL_API_KEY",
    authDomain: "your-project-id.firebaseapp.com",
    projectId: "your-project-id",
    storageBucket: "your-project-id.appspot.com",
    messagingSenderId: "YOUR_MESSAGING_ID",
    appId: "YOUR_APP_ID"
};
```

4. Save the file

## Step 6: Deploy

```bash
git add index.html
git commit -m "Configure Firebase authentication"
git push
```

Wait 30-60 seconds for GitHub Pages to rebuild.

## Step 7: Test

1. Visit your GitHub Pages URL: `https://yourusername.github.io/db`
2. You should see the authentication screen
3. Enter the email and password you created in Step 3
4. Click **"Sign In"**
5. You should be authenticated and see the database interface

## Managing Users

### Add More Users

1. Go to Firebase Console → Authentication → Users
2. Click **"Add user"**
3. Enter email and password
4. Click **"Add user"**

### Remove Users

1. Go to Firebase Console → Authentication → Users
2. Find the user you want to remove
3. Click the three dots menu
4. Click **"Delete user"**

### Reset Password

1. Have the user visit: `https://your-project-id.firebaseapp.com/__/auth/action`
2. Or use Firebase Console to reset manually

## Security Notes

### ✅ What's Secure:

- **Passwords are hashed** server-side by Google
- **No credentials in source code**
- **Token-based authentication** with automatic refresh
- **Can revoke access** instantly via Firebase Console
- **Brute-force protection** built into Firebase

### 🔐 Best Practices:

1. **Use strong passwords** for your Firebase users
2. **Limit user accounts** to only people who need access
3. **Keep repository private** for extra security layer
4. **Monitor authentication logs** in Firebase Console
5. **Enable 2FA** on your Google account (protects Firebase access)

### ⚠️ Limitations:

- **API key is public** - This is normal and safe for Firebase
- **Still client-side app** - Advanced users could theoretically bypass (but can't authenticate without valid credentials)
- **GitHub Pages is public** - Anyone can try to access, but only authorized users can authenticate

## Advanced: Security Rules

For extra security, you can add Firebase Security Rules:

1. Go to Firebase Console → Firestore Database
2. Click **"Rules"** tab
3. Set strict rules to only allow authenticated users

## Troubleshooting

### "Firebase not defined" error
- Check that firebaseConfig is properly set
- Ensure you have internet connection (Firebase CDN loads)

### "Invalid email or password"
- Verify email is exactly as entered in Firebase Console
- Check password is correct (case-sensitive)
- Ensure Email/Password auth is enabled in Firebase

### "Network error"
- Check internet connection
- Verify Firebase project is active
- Check browser console for specific errors

### Authentication works but database doesn't load
- This is a separate issue from authentication
- Check browser console for DuckDB errors
- Verify parquet files are accessible

## Cost

Firebase Authentication free tier includes:
- **10,000 verifications per month**
- **Unlimited users**
- **Phone auth not included** (email/password is free)

For personal use (you + maybe a few teammates), you'll never hit the limit.

## Need Help?

- [Firebase Auth Documentation](https://firebase.google.com/docs/auth)
- [Firebase Console](https://console.firebase.google.com/)
- [GitHub Issues](https://github.com/jbtgames/db/issues)
