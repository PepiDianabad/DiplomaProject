import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import React, { useState } from 'react';
import Home from './components/Home';
import Interview from './components/Interview';
import Results from './components/Results';
import SignIn from './components/SignIn';
import Profile from './components/Profile';
import SignUp from './components/SignUp';


function App() {
  const [user, setUser] = useState(null); // manage user state

  return (
    <Router>  
      <Routes>
        <Route path="/" element={<Home user={user} setUser={setUser} />} />
        <Route path="/interview" element={<Interview />} />
        <Route path="/results" element={<Results />} />
        <Route path="/signin" element={<SignIn setUser={setUser} />} />
        <Route path="/signup" element={<SignUp setUser={setUser}/>} />
        <Route path="/profile" element={user ? <Profile user={user} /> : <SignIn setUser={setUser} />} />
      </Routes>
    </Router>
  );
}

export default App;
