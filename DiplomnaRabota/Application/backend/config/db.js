const { Sequelize } = require('sequelize');

const sequelize = new Sequelize('interview_prep_db', 'postgres', 'password', {
  host: 'postgres',  
  dialect: 'postgres',
  port: 5432,  
  logging: false, 
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
