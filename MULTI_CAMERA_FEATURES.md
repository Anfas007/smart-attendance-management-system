# Multi-Camera System Implementation

## Overview
This document describes the multi-camera system implemented for the attendance tracking application, enabling dynamic camera management, activation/deactivation, and scalability across multiple locations.

## Features Implemented

### 1. Enhanced Camera Model
**Location:** `core/models.py` - Camera model

**New Fields:**
- `camera_type` - Choice field (USB/IP camera)
- `status` - Choice field (active/inactive/offline)
- `ip_address` - IP address for network cameras
- `port` - Port number for IP cameras
- `stream_url` - Full RTSP/HTTP stream URL
- `device_index` - USB camera device index (0, 1, 2, etc.)
- `resolution_width` - Camera resolution width (default: 640)
- `resolution_height` - Camera resolution height (default: 480)
- `fps` - Frames per second (default: 30)
- `is_default` - Boolean to mark default camera
- `created_at` - Auto-timestamp for creation
- `updated_at` - Auto-timestamp for last update

**Features:**
- Automatic enforcement of single default camera
- Support for both USB and IP/Network cameras
- Configurable resolution and frame rate
- Status tracking (active, inactive, offline)

### 2. Camera Management Interface

#### Manage Cameras View
**URL:** `/dashboard/cameras/`
**Template:** `core/templates/core/manage_cameras.html`

**Features:**
- List all cameras with status indicators
- Display camera type (USB/IP)
- Show default camera with star icon
- Color-coded status badges (active/inactive/offline)
- Quick action buttons:
  - Test Connection - Verify camera accessibility
  - Toggle Status - Activate/deactivate camera
  - Set Default - Make camera the default
  - Edit - Modify camera configuration
  - Delete - Remove camera from system

**Filtering:**
- Filter by camera type (USB/IP)
- Filter by status (active/inactive/offline)
- Filter by default camera

#### Add/Edit Camera View
**URL:** 
- Add: `/dashboard/cameras/add/`
- Edit: `/dashboard/cameras/edit/<camera_id>/`
**Template:** `core/templates/core/add_edit_camera.html`

**Features:**
- Dynamic form based on camera type selection
- USB Camera Configuration:
  - Device index selection (0-10)
  - Device detection information
- IP Camera Configuration:
  - IP address input with validation
  - Port number (optional)
  - Stream URL (RTSP/HTTP)
  - Connection examples and help text
- Common Settings:
  - Resolution configuration (width × height)
  - FPS (frames per second)
  - Status selection
  - Default camera checkbox
- Real-time form field visibility based on camera type
- Type-specific validation
- Duplicate name prevention

### 3. Camera Management APIs

**New URL Endpoints:**
```python
# Camera CRUD
/dashboard/cameras/                          # List cameras
/dashboard/cameras/add/                      # Add new camera
/dashboard/cameras/edit/<camera_id>/        # Edit camera
/dashboard/cameras/delete/<camera_id>/      # Delete camera (POST)

# Camera Control
/dashboard/cameras/toggle/<camera_id>/      # Toggle active/inactive (POST)
/dashboard/cameras/set-default/<camera_id>/ # Set as default (POST)
/dashboard/cameras/test/<camera_id>/        # Test connection (POST)
```

**New View Functions:**
- `add_camera_view()` - Create new camera with validation
- `edit_camera_view()` - Update camera configuration
- `toggle_camera_status()` - Switch camera active/inactive
- `set_default_camera()` - Set camera as default
- `test_camera_connection()` - Test camera connectivity

### 4. Multi-Camera Face Attendance

**Enhanced Template:** `core/templates/core/face_attendance.html`

**New Features:**
- Camera selection dropdown
  - Shows all available cameras
  - Indicates default camera
  - Shows camera status
  - Displays camera type and location
- Dynamic camera switching
  - Restart recognition when changing cameras
  - Preserve recognition session
- Browser-based camera access
  - Enumerate available video devices
  - Select specific USB camera by index
  - Fallback for IP cameras (note: direct RTSP not supported in browsers)
- Camera ID passed to backend for tracking

**JavaScript Enhancements:**
- Camera enumeration using MediaDevices API
- Dynamic device selection based on camera configuration
- Automatic camera restart on selection change
- Error handling for camera access failures

### 5. Admin Dashboard Integration

**Enhanced:** `core/templates/core/admin_dashboard.html`

**New Statistics:**
- Total Cameras card - Shows total camera count
- Active Cameras card - Shows number of active cameras
- Camera Status Section:
  - Grid view of up to 6 cameras
  - Visual status indicators (color-coded)
  - Camera type badges
  - Default camera marking
  - Location display
  - Quick link to camera management

**Context Updates:**
- `total_cameras` - Total camera count
- `active_cameras` - Count of active cameras
- `cameras` - Query set of top 6 cameras (ordered by default, status, name)

### 6. Database Migration

**Migration:** `core/migrations/0009_enhance_camera_model.py`

**Changes:**
- Added all new fields to Camera model
- Set appropriate defaults for existing records
- Maintained data integrity during migration

**Applied:** Migration successfully applied to database

## Camera Types

### USB Cameras
- **Configuration:** Device index (0-10)
- **Access Method:** Browser getUserMedia API
- **Pros:** Simple setup, direct browser access
- **Cons:** Limited to local machine, index-based selection
- **Best For:** Single workstation setups

### IP/Network Cameras
- **Configuration:** IP address, port, stream URL
- **Access Method:** RTSP/HTTP streaming (requires backend processing)
- **Pros:** Remote access, multiple locations, professional cameras
- **Cons:** More complex setup, browser limitations for RTSP
- **Best For:** Multi-location deployments, security cameras
- **Note:** Direct browser RTSP access not supported; requires backend streaming proxy or WebRTC conversion

## Usage Workflow

### Adding a Camera

1. Navigate to Admin Dashboard → Cameras (or `/dashboard/cameras/`)
2. Click "Add New Camera"
3. Select camera type (USB or IP)
4. Fill in required fields:
   - **USB:** Name, Location, Device Index
   - **IP:** Name, Location, IP Address, Stream URL
5. Configure optional settings (resolution, FPS, status)
6. Check "Set as Default Camera" if desired
7. Click "Save Camera"

### Managing Cameras

1. Navigate to Manage Cameras
2. View all cameras with status
3. Use quick actions:
   - **Test:** Verify camera connection
   - **Toggle:** Activate/deactivate camera
   - **Star:** Set as default
   - **Edit:** Modify configuration
   - **Delete:** Remove camera

### Using Multiple Cameras for Attendance

1. Navigate to Face Attendance page
2. Select desired camera from dropdown
3. Click "Start Recognition"
4. System will use selected camera for face detection
5. Change camera anytime (will restart recognition)

## Technical Architecture

### Models
```python
class Camera(models.Model):
    CAMERA_TYPES = [('usb', 'USB Camera'), ('ip', 'IP Camera')]
    STATUS_CHOICES = [('active', 'Active'), ('inactive', 'Inactive'), ('offline', 'Offline')]
    
    camera_type = CharField(max_length=10, choices=CAMERA_TYPES, default='usb')
    status = CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    is_default = BooleanField(default=False)
    # ... other fields
```

### Views Pattern
```python
@login_required
@user_passes_test(is_admin)
def camera_management_view(request):
    # Query cameras with filters
    # Handle POST for actions
    # Return template with context
```

### Frontend Integration
```javascript
// Camera selection and initialization
const cameraSelect = document.getElementById('camera-select');
const selectedCamera = cameraSelect.options[cameraSelect.selectedIndex];
const cameraType = selectedCamera.getAttribute('data-type');
const deviceIndex = selectedCamera.getAttribute('data-device-index');

// Dynamic camera switching
cameraSelect.addEventListener('change', () => {
    if (stream) {
        stopCamera();
        setTimeout(() => startCamera(), 100);
    }
});
```

## Security Considerations

1. **Access Control:** All camera management functions require admin authentication
2. **CSRF Protection:** All POST requests include CSRF tokens
3. **Validation:** Type-specific validation for USB vs IP cameras
4. **Unique Names:** Duplicate camera names prevented
5. **Default Camera:** Only one camera can be default at a time

## Scalability

### Current Support
- Unlimited camera registration
- USB cameras: Limited by local USB ports (typically 0-10)
- IP cameras: Unlimited network cameras
- Multi-location support via IP cameras

### Performance Considerations
- Frontend: Browser device enumeration (fast)
- Backend: Face recognition processing (per-camera overhead)
- Database: Indexed queries for camera lookups
- Network: IP camera stream bandwidth

### Recommended Limits
- **Small Setup:** 1-3 USB cameras per workstation
- **Medium Setup:** 5-10 IP cameras across 2-3 locations
- **Large Setup:** 20+ IP cameras with load balancing

## Future Enhancements

### Potential Additions
1. **IP Camera Stream Proxy:** Backend service to convert RTSP to WebRTC/HTTP for browser access
2. **Camera Health Monitoring:** Automatic status updates based on connectivity checks
3. **Camera Groups:** Organize cameras by building/floor/department
4. **Recording:** Store camera feeds for audit purposes
5. **Multi-Camera Recognition:** Simultaneous face recognition across multiple cameras
6. **Analytics Dashboard:** Camera usage statistics and performance metrics
7. **PTZ Control:** Pan-tilt-zoom controls for supported IP cameras
8. **Motion Detection:** Alert on motion in restricted hours

### Known Limitations
1. **Browser RTSP:** Direct RTSP stream access not supported in browsers
2. **USB Camera Selection:** Browser API doesn't allow direct index selection (uses device enumeration)
3. **Concurrent Recognition:** Current implementation processes one camera at a time
4. **Stream Quality:** No dynamic quality adjustment based on bandwidth

## Testing

### Manual Testing Checklist
- [ ] Add USB camera
- [ ] Add IP camera
- [ ] Edit camera configuration
- [ ] Delete camera
- [ ] Toggle camera status
- [ ] Set default camera
- [ ] Test camera connection
- [ ] Select camera in face attendance
- [ ] Switch between cameras during recognition
- [ ] View camera status on admin dashboard
- [ ] Filter cameras by type/status

### Test Cases
1. Create camera with duplicate name (should fail)
2. Set multiple default cameras (only one should remain default)
3. Delete default camera (another should become default)
4. Add IP camera without stream URL (should fail)
5. Switch camera during active recognition (should restart gracefully)

## Deployment Notes

### Requirements
- Python packages: No additional requirements (uses existing cv2, face_recognition)
- Database: Migration 0009 must be applied
- Browser: getUserMedia API support (Chrome, Firefox, Edge, Safari)

### Configuration
No additional settings required. All configuration is database-driven through the admin interface.

### Migration
```bash
python manage.py migrate
```

## Support

### Troubleshooting

**Camera not detected:**
- Check USB connection (for USB cameras)
- Verify IP address and stream URL (for IP cameras)
- Test camera access permissions in browser
- Review browser console for errors

**Cannot select specific USB camera:**
- Browser API limitation - use device enumeration
- Consider using different device indices
- Check camera order in system settings

**IP camera stream not working:**
- Verify RTSP/HTTP URL is correct
- Check network connectivity
- Consider using backend streaming proxy
- Test with VLC or other RTSP client first

**Default camera not working:**
- Ensure at least one camera is marked as default
- Check camera status is "active"
- Verify camera is accessible

## Conclusion

The multi-camera system provides a robust foundation for scalable attendance tracking across multiple locations. With support for both USB and IP cameras, dynamic configuration, and an intuitive management interface, the system can grow from single-workstation setups to enterprise-wide deployments.
