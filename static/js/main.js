// Global variables
let watchId = null;
let currentLocation = null;
let panicButtonPressed = false;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initGeolocation();
    initMotionDetection();
    initPanicButton();
});

// Geolocation tracking
function initGeolocation() {
    if ('geolocation' in navigator) {
        watchId = navigator.geolocation.watchPosition(
            updateLocation,
            handleLocationError,
            { enableHighAccuracy: true, maximumAge: 30000, timeout: 27000 }
        );
    }
}

function updateLocation(position) {
    currentLocation = {
        lat: position.coords.latitude,
        lon: position.coords.longitude,
        accuracy: position.coords.accuracy
    };
    
    // Update display
    const locationDisplay = document.getElementById('location-display');
    if (locationDisplay) {
        locationDisplay.innerHTML = `📍 ${currentLocation.lat.toFixed(6)}, ${currentLocation.lon.toFixed(6)}`;
    }
    
    // Auto-check safety every 5 minutes
    checkLocationSafety();
}

function handleLocationError(error) {
    console.error('Geolocation error:', error);
    showToast('Unable to get your location. Please enable GPS.', 'error');
}

// Check safety based on location
async function checkLocationSafety() {
    if (!currentLocation) return;
    
    try {
        const response = await fetch('/api/check-safety', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(currentLocation)
        });
        
        const data = await response.json();
        if (data.risk > 70) {
            showHighRiskAlert(data);
        }
    } catch (error) {
        console.error('Safety check failed:', error);
    }
}

// Motion detection for automatic alerts
function initMotionDetection() {
    if ('DeviceMotionEvent' in window) {
        let lastX = null;
        let lastY = null;
        let motionCount = 0;
        
        window.addEventListener('devicemotion', function(e) {
            const acc = e.accelerationIncludingGravity;
            const x = Math.abs(acc.x);
            const y = Math.abs(acc.y);
            
            if (x > 20 || y > 20) {
                motionCount++;
                if (motionCount > 3) {
                    triggerEmergency('motion');
                    motionCount = 0;
                }
            } else {
                motionCount = Math.max(0, motionCount - 1);
            }
        });
    }
}

// Panic button functionality
function initPanicButton() {
    const panicBtn = document.getElementById('panic-btn');
    if (panicBtn) {
        panicBtn.addEventListener('click', triggerEmergency.bind(null, 'manual'));
    }
}

async function triggerEmergency(type) {
    if (panicButtonPressed) return;
    panicButtonPressed = true;
    
    // Show confirmation dialog
    const confirmed = confirm('⚠️ EMERGENCY ALERT!\n\nAre you in danger? Press OK to send alert to guardians.');
    
    if (confirmed) {
        showEmergencyPopup();
        
        // Get location if available
        let location = currentLocation;
        if (!location) {
            location = await getCurrentPosition();
        }
        
        // Send to server
        try {
            const response = await fetch('/panic', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    latitude: location.lat,
                    longitude: location.lon,
                    alert_type: type
                })
            });
            
            const data = await response.json();
            if (data.status === 'success') {
                showToast('🚨 Emergency alert sent to your guardians!', 'danger');
            }
        } catch (error) {
            console.error('Failed to send alert:', error);
            showToast('Failed to send alert. Please check your connection.', 'error');
        }
    }
    
    panicButtonPressed = false;
}

function showEmergencyPopup() {
    // Create popup
    const popup = document.createElement('div');
    popup.className = 'alert-popup';
    popup.innerHTML = `
        <h3 style="color: #f44336;">🚨 EMERGENCY ALERT</h3>
        <p>Your location is being shared with your guardians.</p>
        <p>Help is on the way!</p>
        <div class="spinner"></div>
        <button onclick="this.parentElement.remove()" class="btn btn-primary" style="margin-top: 1rem;">OK</button>
    `;
    
    const overlay = document.createElement('div');
    overlay.className = 'alert-overlay';
    
    document.body.appendChild(overlay);
    document.body.appendChild(popup);
    
    // Auto-remove after 10 seconds
    setTimeout(() => {
        popup.remove();
        overlay.remove();
    }, 10000);
}

function showHighRiskAlert(data) {
    const popup = document.createElement('div');
    popup.className = 'alert-popup';
    popup.innerHTML = `
        <h3 style="color: #ff9800;">⚠️ HIGH RISK AREA</h3>
        <p>You are in a high-risk area.</p>
        <p>Risk Level: ${data.risk}%</p>
        <button onclick="triggerEmergency('auto')" class="btn btn-danger" style="margin-top: 1rem;">Emergency Help</button>
        <button onclick="this.parentElement.remove()" class="btn btn-primary" style="margin-top: 1rem;">I'm Safe</button>
    `;
    
    const overlay = document.createElement('div');
    overlay.className = 'alert-overlay';
    
    document.body.appendChild(overlay);
    document.body.appendChild(popup);
}

// Helper functions
function getCurrentPosition() {
    return new Promise((resolve, reject) => {
        if (!navigator.geolocation) {
            reject(new Error('Geolocation not supported'));
            return;
        }
        
        navigator.geolocation.getCurrentPosition(
            position => resolve({
                lat: position.coords.latitude,
                lon: position.coords.longitude
            }),
            error => reject(error),
            { enableHighAccuracy: true, timeout: 10000 }
        );
    });
}

function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    
    const colors = {
        success: '#4caf50',
        error: '#f44336',
        danger: '#f44336',
        info: '#2196f3'
    };
    
    toast.style.background = colors[type] || colors.info;
    document.body.appendChild(toast);
    
    setTimeout(() => toast.remove(), 3000);
}

// Voice detection (if supported)
if ('webkitSpeechRecognition' in window) {
    const recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.onresult = function(event) {
        const text = event.results[event.results.length - 1][0].transcript.toLowerCase();
        if (text.includes('help') || text.includes('emergency') || text.includes('danger')) {
            triggerEmergency('voice');
        }
    };
    recognition.start();
}

// Auto-refresh alerts every 30 seconds
setInterval(() => {
    const alertsContainer = document.getElementById('alerts-list');
    if (alertsContainer) {
        fetch('/api/alerts')
            .then(res => res.json())
            .then(data => updateAlertsList(data));
    }
}, 30000);

function updateAlertsList(alerts) {
    const container = document.getElementById('alerts-list');
    if (!container) return;
    
    container.innerHTML = alerts.map(alert => `
        <div class="alert-item ${alert.status === 'active' ? 'active' : 'resolved'}">
            <div class="alert-info">
                <strong>${alert.alert_type.toUpperCase()}</strong>
                <span>Risk: ${alert.risk_level}%</span>
                <small>${new Date(alert.created_at).toLocaleString()}</small>
            </div>
            <button onclick="resolveAlert(${alert.id})" class="btn btn-sm">Resolve</button>
        </div>
    `).join('');
}
