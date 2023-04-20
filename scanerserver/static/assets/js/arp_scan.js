// Contenido de arp_scan.js
document.addEventListener('DOMContentLoaded', function() {
    var selectDeviceButtons = document.getElementsByClassName('select-device');
    var deviceModal = document.getElementById('device-modal');
  
    for (var i = 0; i < selectDeviceButtons.length; i++) {
      selectDeviceButtons[i].addEventListener('click', function() {
        var ip = this.getAttribute('data-ip');
        var mac = this.getAttribute('data-mac');
        var manufacturer = this.getAttribute('data-manufacturer');
  
        document.getElementById('id_ip_address').value = ip;
        document.getElementById('id_mac_address').value = mac;
        document.getElementById('id_manufacturer').value = manufacturer;
  
        deviceModal.style.display = 'block';
      });
    }
  
    window.addEventListener('click', function(event) {
      if (event.target == deviceModal) {
        deviceModal.style.display = 'none';
      }
    });
  
    deviceModal.addEventListener('click', function(event) {
      if (event.target == deviceModal) {
        deviceModal.style.display = 'none';
      }
    });
  });
  