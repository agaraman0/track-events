import React, { useState } from 'react';
import { Button, TextField, Typography, IconButton } from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import axios from 'axios';

const TrackingPlanForm = () => {
    const [trackingPlan, setTrackingPlan] = useState({
        name: '',
        description: '',
        rules: {
            events: [
                {
                    name: '',
                    description: '',
                    rules: '',
                },
            ],
        }
    });

    const handleChange = (event, index) => {
        const { name, value } = event.target;
        if (name === 'name' || name === 'description') {
            setTrackingPlan({
                ...trackingPlan,
                [name]: value,
            });
        } else {
            const updatedEvents = [...trackingPlan.rules.events];
            updatedEvents[index][name] = value;
            setTrackingPlan({
                ...trackingPlan,
                rules: {
                    ...trackingPlan.rules,
                    events: updatedEvents,
                },
            });
        }
    };

    const handleAddEvent = () => {
        setTrackingPlan({
            ...trackingPlan,
            rules: {
                ...trackingPlan.rules,
                events: [
                    ...trackingPlan.rules.events,
                    {
                        name: '',
                        description: '',
                        rules: '',
                    },
                ],
            },
        });
    };

    const handleSubmit = async () => {
        try {
            const response = await axios.post('http://localhost:5000/tracking-plans/v1/', trackingPlan);
            console.log('Response:', response.data);
        } catch (error) {
            console.error('Error submitting form:', error);
        }
    };

    return (
        <div style={{ margin: '20px' }}>
            <Typography variant="h5">Add Tracking Plan</Typography>
            <TextField
                label="Name"
                name="name"
                variant="outlined"
                fullWidth
                style={{ marginBottom: '10px' }}
                onChange={(event) => handleChange(event)}
            />
            <TextField
                label="Description"
                name="description"
                variant="outlined"
                fullWidth
                style={{ marginBottom: '10px' }}
                onChange={(event) => handleChange(event)}
            />

            <Typography variant="h5">Events</Typography>
            {trackingPlan.rules.events.map((event, index) => (
                <div key={index} style={{ marginBottom: '10px' }}>
                    <TextField
                        label="Name"
                        name="name"
                        variant="outlined"
                        fullWidth
                        style={{ marginBottom: '10px' }}
                        onChange={(event) => handleChange(event, index)}
                    />
                    <TextField
                        label="Description"
                        name="description"
                        variant="outlined"
                        fullWidth
                        style={{ marginBottom: '10px' }}
                        onChange={(event) => handleChange(event, index)}
                    />
                    <TextField
                        label="Rules"
                        name="rules"
                        variant="outlined"
                        fullWidth
                        multiline
                        rows={4}
                        style={{ marginBottom: '10px' }}
                        onChange={(event) => handleChange(event, index)}
                    />
                </div>
            ))}

            <IconButton
                color="primary"
                aria-label="add event"
                component="span"
                onClick={handleAddEvent}
                style={{ backgroundColor: 'blue', marginRight: '10px' }}
            >
                <AddIcon />
            </IconButton>

            <Button variant="contained" color="primary" onClick={handleSubmit}>
                Save
            </Button>
        </div>
    );
};

export default TrackingPlanForm;
