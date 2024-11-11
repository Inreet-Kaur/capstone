import './App.css';
import React from 'react';
import Poc from './viewConnectors/pocConnector';

function App() {
  return (
    <div>
      <header className="flex items-center justify-center text-3xl font-bold">
        RapidCare - POC DEMO 
      </header>
      <body>
        <Poc />
      </body>
    </div>
  );
}

export default App;
