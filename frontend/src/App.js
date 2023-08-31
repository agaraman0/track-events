import React from 'react';
import TrackingPlanForm from './components/TrackingPlanForm';

function App() {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <div style={{ width: '50%', border: '1px solid #ddd', padding: '20px', borderRadius: '10px', backgroundColor: '#f9f9f9' }}>
            <TrackingPlanForm/>
        </div>
    </div>
      
    );
};

export default App;
