# FRC ComponentHub API

A FastAPI-based inventory management system designed specifically for **FIRST Robotics Competition (FRC) teams** to track their components, parts, and inventory.

## 🎯 **Purpose**

This API helps FRC teams:
- 📦 **Track team inventory** - Know exactly what parts you have and where they're stored
- 🛒 **Access public component catalog** - Browse common FRC parts with pricing and vendor info
- 💰 **Budget management** - Track costs and plan purchases
- 📍 **Locate parts** - Find where components are stored in your workspace
- 👥 **Team collaboration** - Multiple team members can manage inventory

## 🛠️ **Features**

### **Public Component Catalog**
A shared database of 46+ real FRC components including:
- ⚡ **Motors** (NEO, Falcon 500, CIM, etc.)
- 🎮 **Motor Controllers** (SPARK MAX, Talon SRX, etc.)
- 🔌 **Electronics** (roboRIO, Power Distribution Hub, etc.)
- 💨 **Pneumatics** (Solenoids, Pneumatic Hub, etc.)
- ⚙️ **Mechanical** (Gearboxes, Wheels, Frame materials, etc.)
- 📡 **Sensors** (Encoders, Cameras, IMU, etc.)

### **Team Inventory Management**
Each team can:
- ✅ Add components to their inventory
- 📊 Track quantities and locations
- 📝 Add team-specific notes
- 🔗 Link to public components for easy data entry
- 👤 Track who added each item

## 📚 **API Documentation**

**Live API**: https://frc-components-api.onrender.com  
**Interactive Docs**: https://frc-components-api.onrender.com/docs  

The API includes 13 endpoints for full CRUD operations on FRC components and team inventory management.