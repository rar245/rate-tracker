import React, { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import data from './data/rates.json';

export default function BankTracker() {
  const [balance, setBalance] = useState(10000);
  const latest = data[data.length - 1];
  const lostInterest = (balance * (latest.Marcus - latest.Chase) / 100).toFixed(2);

  return (
    <div style={{ maxWidth: '800px', margin: 'auto', padding: '20px', fontFamily: 'sans-serif' }}>
      <h1>Bank Rate Archive 🏦</h1>
      <p>Tracking the "Big Bank" interest gap since 2018.</p>
      
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <XAxis dataKey="date" />
          <YAxis unit="%" />
          <Tooltip />
          <Line type="monotone" dataKey="Ally" stroke="#5a2d81" />
          <Line type="monotone" dataKey="Marcus" stroke="#00833e" />
          <Line type="step" dataKey="Chase" stroke="#117aca" strokeWidth={3} />
        </LineChart>
      </ResponsiveContainer>

      <div style={{ background: '#f0f0f0', padding: '20px', borderRadius: '10px', marginTop: '20px' }}>
        <h3>Your "Loyalty Tax" Calculator</h3>
        <input 
          type="number" 
          value={balance} 
          onChange={(e) => setBalance(e.target.value)} 
          style={{ padding: '10px', fontSize: '1.2rem' }}
        />
        <h2 style={{ color: 'red' }}>-${lostInterest} / year</h2>
        <p>This is how much interest you're losing by staying with Chase.</p>
      </div>
    </div>
  );
}
