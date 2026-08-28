#!/bin/bash

# Quantum Logistics Optimizer - Quick Deployment Script

echo "🚀 Quantum Logistics Optimizer - Deployment Script"
echo "=================================================="
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Menu
echo "Select deployment platform:"
echo "1. Streamlit Cloud (Recommended for quick demo)"
echo "2. Heroku"
echo "3. Docker (Local)"
echo "4. AWS EC2 Setup Instructions"
echo "5. Exit"
echo ""
read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo ""
        echo "📦 Preparing for Streamlit Cloud deployment..."
        echo ""
        echo "Steps to deploy on Streamlit Cloud:"
        echo "1. Push your code to GitHub:"
        echo "   git add ."
        echo "   git commit -m 'Prepare for deployment'"
        echo "   git push origin main"
        echo ""
        echo "2. Go to https://share.streamlit.io"
        echo "3. Sign in with GitHub"
        echo "4. Click 'New app'"
        echo "5. Select your repository"
        echo "6. Set main file path: frontend/streamlit_app.py"
        echo "7. Click 'Deploy'"
        echo ""
        echo "✅ Configuration files are ready!"
        ;;
    
    2)
        echo ""
        echo "🔧 Deploying to Heroku..."
        
        if ! command_exists heroku; then
            echo "❌ Heroku CLI not found. Please install it first:"
            echo "   https://devcenter.heroku.com/articles/heroku-cli"
            exit 1
        fi
        
        echo ""
        read -p "Enter your Heroku app name: " app_name
        
        echo ""
        echo "Creating Heroku app..."
        heroku create $app_name
        
        echo ""
        echo "Setting buildpack..."
        heroku buildpacks:set heroku/python -a $app_name
        
        echo ""
        echo "Deploying..."
        git add .
        git commit -m "Deploy to Heroku"
        git push heroku main
        
        echo ""
        echo "✅ Deployment complete!"
        echo "Opening app..."
        heroku open -a $app_name
        ;;
    
    3)
        echo ""
        echo "🐳 Building and running Docker container..."
        
        if ! command_exists docker; then
            echo "❌ Docker not found. Please install Docker first:"
            echo "   https://docs.docker.com/get-docker/"
            exit 1
        fi
        
        echo ""
        echo "Building Docker image..."
        docker build -f Dockerfile.streamlit -t quantum-logistics:latest .
        
        echo ""
        echo "Running container..."
        docker run -d -p 8501:8501 --name quantum-app quantum-logistics:latest
        
        echo ""
        echo "✅ Container started!"
        echo "Access your app at: http://localhost:8501"
        echo ""
        echo "Useful commands:"
        echo "  View logs: docker logs quantum-app"
        echo "  Stop: docker stop quantum-app"
        echo "  Remove: docker rm quantum-app"
        ;;
    
    4)
        echo ""
        echo "☁️  AWS EC2 Deployment Instructions"
        echo "===================================="
        echo ""
        echo "1. Launch EC2 Instance:"
        echo "   - AMI: Ubuntu Server 22.04 LTS"
        echo "   - Instance Type: t2.medium (2 vCPU, 4GB RAM)"
        echo "   - Security Group: Allow ports 22 (SSH) and 8501"
        echo ""
        echo "2. Connect to instance:"
        echo "   ssh -i your-key.pem ubuntu@your-ec2-ip"
        echo ""
        echo "3. Setup:"
        echo "   sudo apt update && sudo apt upgrade -y"
        echo "   sudo apt install python3-pip python3-venv git -y"
        echo "   git clone YOUR_REPO_URL"
        echo "   cd YOUR_REPO"
        echo "   python3 -m venv venv"
        echo "   source venv/bin/activate"
        echo "   pip install -r requirements.txt"
        echo ""
        echo "4. Run:"
        echo "   streamlit run frontend/streamlit_app.py --server.port=8501 --server.address=0.0.0.0"
        echo ""
        echo "5. Access at: http://your-ec2-ip:8501"
        echo ""
        echo "📖 See DEPLOYMENT_GUIDE.md for detailed instructions"
        ;;
    
    5)
        echo "Exiting..."
        exit 0
        ;;
    
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "🎉 Done!"
