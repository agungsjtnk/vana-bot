module.exports = {
    apps: [
        {
            name: "my-app",
            script: "./app.js",
            watch: true,
            log_file: "./logs/combined.log", // Lokasi file log
            error_file: "./logs/error.log",   // Lokasi file log error
            env: {
                NODE_ENV: "production",
            },
        },
    ],
};
