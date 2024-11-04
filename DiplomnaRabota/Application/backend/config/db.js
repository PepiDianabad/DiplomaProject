const { Sequelize } = require('sequelize');

// connection details
const sequelize = new Sequelize('interview_prep_db', 'postgres', 'password', {
  host: 'postgres',  
  dialect: 'postgres',
  port: 5432,  
  logging: false, // Set to true if you want to see the SQL queries being executed
});

// connection test
sequelize.authenticate()
  .then(() => {
    console.log('Connected to PostgreSQL database successfully.');
  })
  .catch((err) => {
    console.error('Unable to connect to the database:', err);
  });

module.exports = sequelize;
