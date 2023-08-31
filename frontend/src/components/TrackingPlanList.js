import React from "react";

const TrackingPlanList = () => {
  const trackingPlans = []; // Fetch this from API or state

  return (
    <div>
      <h2>Tracking Plans</h2>
      <ul>
        {trackingPlans.map((plan, index) => (
          <li key={index}>{plan.displayName}</li>
        ))}
      </ul>
    </div>
  );
};

export default TrackingPlanList;
