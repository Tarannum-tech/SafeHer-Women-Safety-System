// // Voice Detection for Emergency (Browser-based)
// let recognition = null;
// let isListening = false;
// let currentLocation = null;

// function initVoiceDetection() {
//     const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
//     if (SpeechRecognition) {
//         recognition = new SpeechRecognition();
//         recognition.continuous = true;
//         recognition.interimResults = true;
//         recognition.lang = 'en-US';
        
//         recognition.onresult = function(event) {
//             let transcript = '';
//             for (let i = event.resultIndex; i < event.results.length; i++) {
//                 transcript += event.results[i][0].transcript;
//             }
            
//             console.log('Heard:', transcript);
            
//             const distressWords = ['help', 'danger', 'save me', 'emergency', 'police', 'attack', 'kidnap', 'follow', 'stalking'];
//             const lowerTranscript = transcript.toLowerCase();
            
//             for (let word of distressWords) {
//                 if (lowerTranscript.includes(word)) {
//                     triggerVoiceEmergency(word);
//                     break;
//                 }
//             }
//         };
        
//         recognition.onerror = function(event) {
//             console.error('Voice recognition error:', event.error);
//         };
        
//         recognition.onend = function() {
//             if (isListening) {
//                 recognition.start();
//             }
//         };
        
//         console.log('✅ Voice detection initialized');
//     } else {
//         console.warn('⚠️ Speech recognition not supported');
//         showToast('Voice detection not supported in this browser', 'warning');
//     }
// }

// function getCurrentLocation() {
//     return new Promise((resolve, reject) => {
//         if (navigator.geolocation) {
//             navigator.geolocation.getCurrentPosition(
//                 (position) => {
//                     currentLocation = {
//                         lat: position.coords.latitude,
//                         lon: position.coords.longitude
//                     };
//                     resolve(currentLocation);
//                 },
//                 (error) => {
//                     console.error('Location error:', error);
//                     resolve(null);
//                 },
//                 { enableHighAccuracy: true, timeout: 10000 }
//             );
//         } else {
//             resolve(null);
//         }
//     });
// }

// async function triggerVoiceEmergency(word) {
//     showToast(`🚨 Emergency detected! Word: "${word}"`, 'danger');
    
//     // Get current location
//     const location = await getCurrentLocation();
    
//     fetch('/voice_detect', {
//         method: 'POST',
//         headers: {'Content-Type': 'application/json'},
//         body: JSON.stringify({
//             text: word,
//             latitude: location ? location.lat : null,
//             longitude: location ? location.lon : null
//         })
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.alert) {
//             if (data.require_login) {
//                 showToast('⚠️ Please login to send emergency alert!', 'warning');
//                 setTimeout(() => {
//                     window.location.href = '/login';
//                 }, 2000);
//             } else if (data.notification) {
//                 showNotificationResult(data.notification);
//             }
            
//             // Trigger emergency alert display
//             if (typeof showEmergencyPopup === 'function') {
//                 showEmergencyPopup();
//             } else {
//                 alert('🚨 EMERGENCY ALERT SENT!\n\nYour location has been shared with:\n- Your Guardians\n- Nearby Police Stations\n- Women Safety NGOs\n\nHelp is on the way!');
//             }
//         }
//     })
//     .catch(error => console.error('Error:', error));
// }

// function showNotificationResult(notification) {
//     let message = '🚨 EMERGENCY ALERT SENT!\n\n';
    
//     if (notification.guardians_notified && notification.guardians_notified.length > 0) {
//         message += `👨‍👩‍👧 Notified Guardians: ${notification.guardians_notified.join(', ')}\n`;
//     }
    
//     if (notification.police_notified && notification.police_notified.length > 0) {
//         message += `👮 Notified Police: ${notification.police_notified.join(', ')}\n`;
//     }
    
//     if (notification.ngos_notified && notification.ngos_notified.length > 0) {
//         message += `🆘 Notified NGOs: ${notification.ngos_notified.join(', ')}\n`;
//     }
    
//     message += '\n📍 Your location has been shared.\nHelp is on the way!';
    
//     alert(message);
// }

// function initShakeDetection() {
//     let lastShake = 0;
//     let shakeCount = 0;
    
//     if (window.DeviceMotionEvent) {
//         window.addEventListener('devicemotion', async function(e) {
//             let acceleration = e.accelerationIncludingGravity;
//             let x = acceleration.x || 0;
//             let y = acceleration.y || 0;
//             let z = acceleration.z || 0;
            
//             let magnitude = Math.sqrt(x*x + y*y + z*z);
            
//             if (magnitude > 25) {
//                 let now = Date.now();
//                 if (now - lastShake < 500) {
//                     shakeCount++;
//                     if (shakeCount >= 3) {
//                         triggerSOSPattern();
//                         shakeCount = 0;
//                     }
//                 } else {
//                     shakeCount = 1;
//                 }
//                 lastShake = now;
//             }
//         });
//         console.log('✅ Shake detection initialized');
//     }
// }

// async function triggerSOSPattern() {
//     showToast('🚨 SOS Pattern detected! Phone shaken 3 times.', 'danger');
    
//     const location = await getCurrentLocation();
    
//     fetch('/sos_pattern', {
//         method: 'POST',
//         headers: {'Content-Type': 'application/json'},
//         body: JSON.stringify({
//             pattern: 'shake',
//             latitude: location ? location.lat : null,
//             longitude: location ? location.lon : null
//         })
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.alert) {
//             if (data.require_login) {
//                 showToast('⚠️ Please login to send emergency alert!', 'warning');
//                 setTimeout(() => {
//                     window.location.href = '/login';
//                 }, 2000);
//             } else if (data.notification) {
//                 showNotificationResult(data.notification);
//             }
            
//             if (typeof showEmergencyPopup === 'function') {
//                 showEmergencyPopup();
//             }
//         }
//     })
//     .catch(error => console.error('Error:', error));
// }

// function showToast(message, type) {
//     let toast = document.createElement('div');
//     toast.className = 'toast-notification';
//     toast.innerHTML = message;
    
//     const colors = {
//         success: '#4caf50',
//         danger: '#dc3545',
//         warning: '#ff9800',
//         info: '#2196f3'
//     };
    
//     toast.style.cssText = `
//         position: fixed;
//         bottom: 100px;
//         right: 20px;
//         background: ${colors[type] || colors.info};
//         color: white;
//         padding: 12px 20px;
//         border-radius: 8px;
//         z-index: 10000;
//         font-size: 14px;
//         font-weight: 500;
//         box-shadow: 0 2px 10px rgba(0,0,0,0.2);
//         animation: slideIn 0.3s ease;
//         max-width: 300px;
//     `;
    
//     document.body.appendChild(toast);
//     setTimeout(() => toast.remove(), 5000);
// }

// const style = document.createElement('style');
// style.textContent = `
//     @keyframes slideIn {
//         from {
//             transform: translateX(100%);
//             opacity: 0;
//         }
//         to {
//             transform: translateX(0);
//             opacity: 1;
//         }
//     }
// `;
// document.head.appendChild(style);

// document.addEventListener('DOMContentLoaded', function() {
//     initVoiceDetection();
//     initShakeDetection();
    
//     // Get current location on load
//     getCurrentLocation();
    
//     // Add voice control button
//     const voiceBtn = document.createElement('button');
//     voiceBtn.innerHTML = '🎤';
//     voiceBtn.style.cssText = `
//         position: fixed;
//         bottom: 100px;
//         right: 90px;
//         width: 50px;
//         height: 50px;
//         border-radius: 50%;
//         background: #ff9800;
//         color: white;
//         border: none;
//         font-size: 20px;
//         cursor: pointer;
//         z-index: 1000;
//         box-shadow: 0 2px 10px rgba(0,0,0,0.2);
//     `;
//     voiceBtn.onclick = function() {
//         if (typeof startVoiceDetection === 'function') {
//             startVoiceDetection();
//             showToast('🎤 Voice detection activated! Say "Help" for emergency.', 'success');
//         }
//     };
//     document.body.appendChild(voiceBtn);
// });

// Voice Detection for Emergency (Browser-based)
let recognition = null;
let isListening = false;
let currentLocation = null;

function initVoiceDetection() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = 'en-US';
        
        recognition.onstart = function() {
            console.log('🎤 Voice recognition started');
            isListening = true;
            updateVoiceStatus(true);
        };
        
        recognition.onend = function() {
            console.log('🎤 Voice recognition ended');
            if (isListening) {
                // Restart if still listening
                recognition.start();
            } else {
                updateVoiceStatus(false);
            }
        };
        
        recognition.onresult = function(event) {
            let transcript = '';
            for (let i = event.resultIndex; i < event.results.length; i++) {
                transcript += event.results[i][0].transcript;
            }
            
            console.log('Heard:', transcript);
            
            const distressWords = ['help', 'danger', 'save me', 'emergency', 'police', 'attack', 'kidnap', 'follow', 'stalking'];
            const lowerTranscript = transcript.toLowerCase();
            
            for (let word of distressWords) {
                if (lowerTranscript.includes(word)) {
                    triggerVoiceEmergency(word);
                    break;
                }
            }
        };
        
        recognition.onerror = function(event) {
            console.error('Voice recognition error:', event.error);
            if (event.error === 'not-allowed') {
                alert('Please allow microphone access for voice detection.');
            }
        };
        
        console.log('✅ Voice detection initialized');
        return true;
    } else {
        console.warn('⚠️ Speech recognition not supported');
        alert('Voice detection not supported in this browser. Please use Chrome, Edge, or Safari.');
        return false;
    }
}

function startListening() {
    if (recognition && !isListening) {
        try {
            recognition.start();
            isListening = true;
            console.log('🎤 Started listening');
            return true;
        } catch (e) {
            console.error('Failed to start:', e);
            return false;
        }
    }
    return false;
}

function stopListening() {
    if (recognition && isListening) {
        try {
            recognition.stop();
            isListening = false;
            console.log('🎤 Stopped listening');
            return true;
        } catch (e) {
            console.error('Failed to stop:', e);
            return false;
        }
    }
    return false;
}

function updateVoiceStatus(isActive) {
    const statusDiv = document.getElementById('voiceStatus');
    const micBtn = document.getElementById('microphoneBtn');
    
    if (statusDiv) {
        if (isActive) {
            statusDiv.classList.add('active');
            statusDiv.innerHTML = '🎤 Listening... Say "Help" for emergency';
            setTimeout(() => {
                if (statusDiv.classList.contains('active')) {
                    statusDiv.innerHTML = '🎤 Voice detection active';
                }
            }, 3000);
        } else {
            statusDiv.classList.remove('active');
        }
    }
    
    if (micBtn) {
        if (isActive) {
            micBtn.classList.add('active');
            micBtn.style.background = 'linear-gradient(135deg, #4caf50, #45a049)';
        } else {
            micBtn.classList.remove('active');
            micBtn.style.background = 'linear-gradient(135deg, #ff9800, #f57c00)';
        }
    }
}

function getCurrentLocation() {
    return new Promise((resolve) => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    currentLocation = {
                        lat: position.coords.latitude,
                        lon: position.coords.longitude
                    };
                    resolve(currentLocation);
                },
                (error) => {
                    console.error('Location error:', error);
                    resolve(null);
                },
                { enableHighAccuracy: true, timeout: 10000 }
            );
        } else {
            resolve(null);
        }
    });
}

async function triggerVoiceEmergency(word) {
    console.log('🚨 Emergency triggered by word:', word);
    
    // Show immediate feedback
    showToast(`🚨 Emergency detected! Word: "${word}"`, 'danger');
    
    // Get current location
    const location = await getCurrentLocation();
    
    try {
        const response = await fetch('/voice_detect', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                text: word,
                latitude: location ? location.lat : null,
                longitude: location ? location.lon : null
            })
        });
        
        const data = await response.json();
        
        if (data.alert) {
            if (data.require_login) {
                showToast('⚠️ Please login to send emergency alert!', 'warning');
                setTimeout(() => {
                    window.location.href = '/login';
                }, 2000);
            } else if (data.notification) {
                showNotificationResult(data.notification);
            } else {
                alert('🚨 EMERGENCY ALERT SENT!\n\nYour location has been shared with:\n- Your Guardians\n- Nearby Police Stations\n- Women Safety NGOs\n\nHelp is on the way!');
            }
        }
    } catch (error) {
        console.error('Error sending alert:', error);
        showToast('Error sending alert. Please check connection.', 'danger');
    }
}

function showNotificationResult(notification) {
    let message = '🚨 EMERGENCY ALERT SENT!\n\n';
    
    if (notification.guardians_notified && notification.guardians_notified.length > 0) {
        message += `👨‍👩‍👧 Notified Guardians: ${notification.guardians_notified.join(', ')}\n`;
    }
    
    if (notification.police_notified && notification.police_notified.length > 0) {
        message += `👮 Notified Police: ${notification.police_notified.join(', ')}\n`;
    }
    
    if (notification.ngos_notified && notification.ngos_notified.length > 0) {
        message += `🆘 Notified NGOs: ${notification.ngos_notified.join(', ')}\n`;
    }
    
    message += '\n📍 Your location has been shared.\nHelp is on the way!';
    
    alert(message);
}

function showToast(message, type) {
    let toast = document.createElement('div');
    toast.className = 'toast-notification';
    toast.innerHTML = message;
    
    const colors = {
        success: '#4caf50',
        danger: '#dc3545',
        warning: '#ff9800',
        info: '#2196f3'
    };
    
    toast.style.cssText = `
        position: fixed;
        bottom: 100px;
        right: 20px;
        background: ${colors[type] || colors.info};
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        z-index: 10000;
        font-size: 14px;
        font-weight: 500;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        animation: slideIn 0.3s ease;
        max-width: 300px;
    `;
    
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 5000);
}

// Shake Detection
function initShakeDetection() {
    let lastShake = 0;
    let shakeCount = 0;
    
    if (window.DeviceMotionEvent) {
        window.addEventListener('devicemotion', async function(e) {
            let acceleration = e.accelerationIncludingGravity;
            let x = Math.abs(acceleration.x || 0);
            let y = Math.abs(acceleration.y || 0);
            let z = Math.abs(acceleration.z || 0);
            
            let magnitude = x + y + z;
            
            if (magnitude > 35) {
                let now = Date.now();
                if (now - lastShake < 500) {
                    shakeCount++;
                    if (shakeCount >= 3) {
                        triggerSOSPattern();
                        shakeCount = 0;
                    }
                } else {
                    shakeCount = 1;
                }
                lastShake = now;
            }
        });
        console.log('✅ Shake detection initialized');
    }
}

async function triggerSOSPattern() {
    showToast('🚨 SOS Pattern detected! Phone shaken 3 times.', 'danger');
    
    const location = await getCurrentLocation();
    
    try {
        const response = await fetch('/sos_pattern', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                pattern: 'shake',
                latitude: location ? location.lat : null,
                longitude: location ? location.lon : null
            })
        });
        
        const data = await response.json();
        
        if (data.alert) {
            if (data.require_login) {
                showToast('⚠️ Please login to send emergency alert!', 'warning');
                setTimeout(() => {
                    window.location.href = '/login';
                }, 2000);
            } else if (data.notification) {
                showNotificationResult(data.notification);
            }
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

// Add CSS for animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
`;
document.head.appendChild(style);

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initVoiceDetection();
    initShakeDetection();
    
    // Get current location on load
    getCurrentLocation();
});