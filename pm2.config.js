module.exports = {
  apps: [
    {
      name: "tonclayton-bot", 
      script: "./index.js", 
      instances: "max", 
      exec_mode: "cluster", 
      watch: false,
      env: {
        NODE_ENV: "production", 
      },
      log_file: './combined.log',
      out_file: './out.log',
      error_file: './err.log',
      time: true,
    },
  ],
};
