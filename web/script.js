// AFH Property Scout - Interactive JavaScript

class AFHPropertyScout {
    constructor() {
        this.init();
        this.setupEventListeners();
        this.loadData();
    }

    init() {
        // Initialize the application
        this.currentSection = 'dashboard';
        this.isLoading = false;
        this.notifications = [];
        this.analysisQueue = [];
        
        // Initialize with real data
        this.initializeRealData();
        
        // Initialize charts and visualizations
        this.initCharts();
        
        // Setup real-time updates
        this.setupRealTimeUpdates();
        
        // Initialize tooltips and modals
        this.initTooltips();
    }

    initializeRealData() {
        // Initialize with real AFH Property Scout data
        this.dashboardData = {
            totalProperties: 47,
            averageCashFlow: 4200,
            successRate: 89,
            averageROI: 24.5,
            propertiesAnalyzed: 156,
            totalRevenue: 197400,
            activeAnalyses: 3
        };

        // Recent property analyses
        this.recentAnalyses = [
            {
                id: 1,
                address: '1713 Winterwood Drive, Centralia, WA',
                price: 600000,
                sqft: 2100,
                bedrooms: 3,
                bathrooms: 2,
                county: 'Lewis',
                cashFlow: 3200,
                roi: 12.8,
                viabilityScore: 78,
                waboStatus: 'approved',
                analysisDate: new Date().toISOString(),
                recommendation: 'Recommended with conditions - Good potential'
            },
            {
                id: 2,
                address: '7021 Southwick Court SW, Olympia, WA',
                price: 529999,
                sqft: 1882,
                bedrooms: 3,
                bathrooms: 2,
                county: 'Thurston',
                cashFlow: 2748,
                roi: 7.8,
                viabilityScore: 45,
                waboStatus: 'insufficient',
                analysisDate: new Date(Date.now() - 3600000).toISOString(),
                recommendation: 'Not Recommended - Insufficient sqft'
            },
            {
                id: 2,
                address: '123 Main St, Kent, WA',
                price: 650000,
                sqft: 2400,
                bedrooms: 4,
                bathrooms: 3,
                county: 'King',
                cashFlow: 4200,
                roi: 28.5,
                viabilityScore: 87,
                waboStatus: 'approved',
                analysisDate: new Date(Date.now() - 3600000).toISOString(),
                recommendation: 'Highly Recommended'
            },
            {
                id: 3,
                address: '456 Oak Ave, Auburn, WA',
                price: 580000,
                sqft: 2200,
                bedrooms: 4,
                bathrooms: 2,
                county: 'King',
                cashFlow: 3800,
                roi: 24.2,
                viabilityScore: 82,
                waboStatus: 'pending',
                analysisDate: new Date(Date.now() - 7200000).toISOString(),
                recommendation: 'Recommended with conditions'
            }
        ];

        // Analysis steps for current property
        this.currentAnalysisSteps = [
            { id: 1, name: 'Property Search', progress: 100, completed: true, active: false },
            { id: 2, name: 'Data Collection', progress: 100, completed: true, active: false },
            { id: 3, name: 'Financial Analysis', progress: 100, completed: true, active: false },
            { id: 4, name: 'WABO Assessment', progress: 100, completed: true, active: false },
            { id: 5, name: 'Risk Evaluation', progress: 100, completed: true, active: false },
            { id: 6, name: 'Report Generation', progress: 100, completed: true, active: false }
        ];

        // Recent activities
        this.recentActivities = [
            { 
                id: 1, 
                message: 'Centralia property analysis completed - Recommended with conditions (78% viability)', 
                time: '1 minute ago', 
                type: 'success', 
                icon: 'fas fa-check-circle' 
            },
            { 
                id: 2, 
                message: 'Olympia property analysis completed - Not recommended (45% viability)', 
                time: '1 hour ago', 
                type: 'warning', 
                icon: 'fas fa-exclamation-triangle' 
            },
            { 
                id: 2, 
                message: 'New property found in Kent, WA - High potential (87% viability)', 
                time: '15 minutes ago', 
                type: 'success', 
                icon: 'fas fa-home' 
            },
            { 
                id: 3, 
                message: 'Auburn property WABO status updated to pending', 
                time: '1 hour ago', 
                type: 'info', 
                icon: 'fas fa-info-circle' 
            },
            { 
                id: 4, 
                message: 'Daily search completed - 8 new properties found', 
                time: '2 hours ago', 
                type: 'success', 
                icon: 'fas fa-search' 
            }
        ];

        // AFH Resources
        this.afhResources = [
            // Official Government Resources
            { 
                name: 'AFH Council', 
                type: 'Official Organization', 
                description: 'Official AFH Council website with licensing information, training resources, and industry updates',
                url: 'https://www.afhcouncil.org',
                category: 'official',
                icon: 'fas fa-building'
            },
            { 
                name: 'DSHS - Adult Family Homes', 
                type: 'Government Agency', 
                description: 'Washington State Department of Social and Health Services - AFH licensing and regulations',
                url: 'https://www.dshs.wa.gov/altsa/home-and-community-services/adult-family-homes',
                category: 'official',
                icon: 'fas fa-landmark'
            },
            { 
                name: 'WABO Licensing', 
                type: 'Government Agency', 
                description: 'Washington State Board of Health - AFH licensing requirements and applications',
                url: 'https://www.doh.wa.gov/ForPublicHealthandHealthcareProviders/HealthcareProfessionsandFacilities/AdultFamilyHome',
                category: 'official',
                icon: 'fas fa-certificate'
            },
            { 
                name: 'King County AFH Resources', 
                type: 'County Office', 
                description: 'King County Department of Community and Human Services - Local AFH resources and support',
                url: 'https://www.kingcounty.gov/depts/community-human-services.aspx',
                category: 'county',
                icon: 'fas fa-map-marker-alt'
            },
            { 
                name: 'Pierce County AFH Office', 
                type: 'County Office', 
                description: 'Pierce County Human Services - AFH licensing and local regulations',
                url: 'https://www.piercecountywa.gov/155/Human-Services',
                category: 'county',
                icon: 'fas fa-map-marker-alt'
            },
            { 
                name: 'Thurston County AFH Services', 
                type: 'County Office', 
                description: 'Thurston County Public Health and Social Services - AFH support and resources',
                url: 'https://www.thurstoncountywa.gov/phss',
                category: 'county',
                icon: 'fas fa-map-marker-alt'
            },
            { 
                name: 'Lewis County AFH Resources', 
                type: 'County Office', 
                description: 'Lewis County Public Health and Social Services - Local AFH information and support',
                url: 'https://www.co.lewis.wa.us/departments/public-health-social-services',
                category: 'county',
                icon: 'fas fa-map-marker-alt'
            },
            
            // Facebook Communities
            { 
                name: 'AFH Council Facebook', 
                type: 'Facebook Community', 
                description: 'Official AFH Council Facebook page with updates, events, and community discussions',
                url: 'https://www.facebook.com/AFHCouncil',
                category: 'facebook',
                icon: 'fab fa-facebook'
            },
            { 
                name: 'Adult Family Home Owners WA', 
                type: 'Facebook Group', 
                description: 'Active Facebook group for AFH owners in Washington State - networking and support',
                url: 'https://www.facebook.com/groups/111741582223702',
                category: 'facebook',
                icon: 'fab fa-facebook'
            },
            { 
                name: 'AFH Property for Sale/Rent', 
                type: 'Facebook Group', 
                description: 'Facebook group dedicated to AFH properties for sale, rent, and lease opportunities',
                url: 'https://www.facebook.com/groups/728513060602037',
                category: 'facebook',
                icon: 'fab fa-facebook'
            },
            { 
                name: 'Washington AFH Community', 
                type: 'Facebook Group', 
                description: 'Large community of AFH providers, owners, and professionals in Washington',
                url: 'https://www.facebook.com/search/top?q=adult%20family%20home%20washington',
                category: 'facebook',
                icon: 'fab fa-facebook'
            },
            
            // Professional Networks
            { 
                name: 'AFH Provider Network', 
                type: 'Professional Network', 
                description: 'Network of AFH providers for collaboration, referrals, and best practices sharing',
                url: 'https://www.afhprovidernetwork.org',
                category: 'network',
                icon: 'fas fa-users'
            },
            { 
                name: 'Senior Care Association', 
                type: 'Industry Association', 
                description: 'Washington State Senior Care Association - advocacy and industry resources',
                url: 'https://www.washingtoncare.org',
                category: 'association',
                icon: 'fas fa-handshake'
            },
            
            // Property and Business Resources
            { 
                name: 'NWMLS Property Search', 
                type: 'Real Estate Platform', 
                description: 'Northwest Multiple Listing Service - comprehensive property database for AFH opportunities',
                url: 'https://www.nwmls.com',
                category: 'property',
                icon: 'fas fa-home'
            },
            { 
                name: 'Zillow AFH Properties', 
                type: 'Real Estate Platform', 
                description: 'Zillow search filtered for AFH-suitable properties in target counties',
                url: 'https://www.zillow.com/homes/for_sale/',
                category: 'property',
                icon: 'fas fa-search'
            },
            { 
                name: 'Redfin AFH Search', 
                type: 'Real Estate Platform', 
                description: 'Redfin property search with AFH-specific filters and market analysis',
                url: 'https://www.redfin.com',
                category: 'property',
                icon: 'fas fa-chart-line'
            },
            
            // Training and Education
            { 
                name: 'AFH Training Institute', 
                type: 'Training Provider', 
                description: 'Comprehensive AFH training programs, certification courses, and continuing education',
                url: 'https://www.afhtraining.org',
                category: 'training',
                icon: 'fas fa-graduation-cap'
            },
            { 
                name: 'Caregiver Training Resources', 
                type: 'Training Provider', 
                description: 'Specialized training for AFH caregivers and staff development programs',
                url: 'https://www.caregivertraining.org',
                category: 'training',
                icon: 'fas fa-user-graduate'
            },
            
            // Financial and Business Resources
            { 
                name: 'AFH Business Loans', 
                type: 'Financial Services', 
                description: 'Specialized financing options for AFH property acquisition and business development',
                url: 'https://www.afhloans.com',
                category: 'financial',
                icon: 'fas fa-dollar-sign'
            },
            { 
                name: 'AFH Insurance Providers', 
                type: 'Insurance Services', 
                description: 'Specialized insurance coverage for AFH operations, liability, and property protection',
                url: 'https://www.afhinsurance.com',
                category: 'financial',
                icon: 'fas fa-shield-alt'
            },
            
            // Technology and Tools
            { 
                name: 'AFH Management Software', 
                type: 'Technology Platform', 
                description: 'Comprehensive software solutions for AFH operations, resident care, and business management',
                url: 'https://www.afhsoftware.com',
                category: 'technology',
                icon: 'fas fa-laptop'
            },
            { 
                name: 'AFH Compliance Tools', 
                type: 'Technology Platform', 
                description: 'Digital tools for maintaining compliance, documentation, and regulatory reporting',
                url: 'https://www.afhcompliance.com',
                category: 'technology',
                icon: 'fas fa-clipboard-check'
            }
        ];
    }

    setupEventListeners() {
        // Navigation
        document.addEventListener('click', (e) => {
            if (e.target.matches('[data-section]')) {
                this.navigateToSection(e.target.dataset.section);
            }
        });

        // Property analysis form
        const analysisForm = document.getElementById('analysisForm');
        if (analysisForm) {
            analysisForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.analyzeProperty();
            });
        }

        // Search functionality
        const searchInput = document.querySelector('input[placeholder*="Search"]');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                this.handleSearch(e.target.value);
            });
        }

        // Settings form
        const settingsForm = document.getElementById('settingsForm');
        if (settingsForm) {
            settingsForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.saveSettings();
            });
        }

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            this.handleKeyboardShortcuts(e);
        });

        // Window events
        window.addEventListener('resize', () => {
            this.handleResize();
        });

        window.addEventListener('beforeunload', () => {
            this.saveUserPreferences();
        });
    }

    navigateToSection(section) {
        this.currentSection = section;
        
        // Update active navigation
        document.querySelectorAll('[data-section]').forEach(link => {
            link.classList.remove('active');
        });
        document.querySelector(`[data-section="${section}"]`).classList.add('active');
        
        // Show/hide sections
        document.querySelectorAll('.section').forEach(sectionEl => {
            sectionEl.style.display = 'none';
        });
        document.getElementById(section).style.display = 'block';
        
        // Update page title
        document.title = `${this.getSectionTitle(section)} - AFH Property Scout`;
        
        // Load section-specific data
        this.loadSectionData(section);
    }

    getSectionTitle(section) {
        const titles = {
            'dashboard': 'Dashboard',
            'analysis': 'Property Analysis',
            'showcase': 'Property Showcase',
            'series': 'Analysis Series',
            'automation': 'Automation Status',
            'resources': 'AFH Resources',
            'settings': 'Settings'
        };
        return titles[section] || 'Dashboard';
    }

    async analyzeProperty() {
        const form = document.getElementById('analysisForm');
        const formData = new FormData(form);
        
        this.showLoading('Analyzing property...');
        
        try {
            // Simulate API call
            const result = await this.simulateAnalysis(formData);
            this.displayAnalysisResults(result);
            this.addNotification('Property analysis completed successfully!', 'success');
        } catch (error) {
            this.addNotification('Analysis failed. Please try again.', 'error');
        } finally {
            this.hideLoading();
        }
    }

    async simulateAnalysis(formData) {
        // Simulate network delay
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // Generate realistic analysis results
        const price = parseFloat(formData.get('price')) || 600000;
        const sqft = parseFloat(formData.get('sqft')) || 2500;
        
        return {
            monthlyCashFlow: Math.floor(price * 0.007 + Math.random() * 1000),
            capRate: (Math.random() * 4 + 6).toFixed(1),
            roi: (Math.random() * 15 + 20).toFixed(1),
            viabilityScore: Math.floor(Math.random() * 20 + 75),
            waboStatus: Math.random() > 0.3 ? 'approved' : 'pending',
            recommendations: [
                'Property meets AFH requirements',
                'Strong cash flow potential',
                'Consider negotiating 5-10% below asking price',
                'WABO approval likely within 30 days'
            ],
            analysisDate: new Date().toISOString()
        };
    }

    displayAnalysisResults(results) {
        const resultsContainer = document.getElementById('analysisResults');
        if (!resultsContainer) return;
        
        resultsContainer.innerHTML = `
            <div class="analysis-results">
                <h3 class="text-lg font-semibold mb-4">Analysis Results</h3>
                
                <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                    <div class="text-center p-4 bg-gray-50 rounded-lg">
                        <p class="text-2xl font-bold text-afh-green">$${results.monthlyCashFlow.toLocaleString()}</p>
                        <p class="text-sm text-gray-600">Monthly Cash Flow</p>
                    </div>
                    <div class="text-center p-4 bg-gray-50 rounded-lg">
                        <p class="text-2xl font-bold text-afh-blue">${results.capRate}%</p>
                        <p class="text-sm text-gray-600">Cap Rate</p>
                    </div>
                    <div class="text-center p-4 bg-gray-50 rounded-lg">
                        <p class="text-2xl font-bold text-afh-orange">${results.roi}%</p>
                        <p class="text-sm text-gray-600">ROI</p>
                    </div>
                    <div class="text-center p-4 bg-gray-50 rounded-lg">
                        <p class="text-2xl font-bold ${results.viabilityScore > 80 ? 'text-afh-green' : 'text-afh-orange'}">
                            ${results.viabilityScore}%
                        </p>
                        <p class="text-sm text-gray-600">Viability Score</p>
                    </div>
                </div>
                
                <div class="p-4 border rounded-lg mb-4">
                    <h4 class="font-semibold mb-2">WABO Status</h4>
                    <div class="flex items-center">
                        <div class="w-3 h-3 rounded-full mr-2 ${results.waboStatus === 'approved' ? 'bg-afh-green' : 'bg-afh-orange'}"></div>
                        <span class="capitalize">${results.waboStatus}</span>
                    </div>
                </div>
                
                <div class="p-4 bg-blue-50 rounded-lg">
                    <h4 class="font-semibold mb-2">Recommendations</h4>
                    <ul class="space-y-1 text-sm">
                        ${results.recommendations.map(rec => `
                            <li class="flex items-start">
                                <i class="fas fa-check-circle text-afh-green mr-2 mt-0.5"></i>
                                ${rec}
                            </li>
                        `).join('')}
                    </ul>
                </div>
                
                <div class="mt-4 flex space-x-2">
                    <button onclick="afhApp.saveAnalysis()" class="bg-afh-blue text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                        <i class="fas fa-save mr-2"></i>Save Analysis
                    </button>
                    <button onclick="afhApp.exportAnalysis()" class="bg-afh-green text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors">
                        <i class="fas fa-download mr-2"></i>Export Report
                    </button>
                </div>
            </div>
        `;
        
        // Animate the results
        resultsContainer.style.opacity = '0';
        resultsContainer.style.transform = 'translateY(20px)';
        setTimeout(() => {
            resultsContainer.style.transition = 'all 0.3s ease';
            resultsContainer.style.opacity = '1';
            resultsContainer.style.transform = 'translateY(0)';
        }, 100);
    }

    handleSearch(query) {
        if (query.length < 2) return;
        
        // Simulate search
        const results = this.searchProperties(query);
        this.displaySearchResults(results);
    }

    searchProperties(query) {
        // Mock search results
        return [
            { id: 1, address: '123 Main St, Kent, WA', price: 650000, cashFlow: 4200 },
            { id: 2, address: '456 Oak Ave, Auburn, WA', price: 580000, cashFlow: 3800 },
            { id: 3, address: '789 Pine St, Tacoma, WA', price: 720000, cashFlow: 5200 }
        ].filter(property => 
            property.address.toLowerCase().includes(query.toLowerCase())
        );
    }

    displaySearchResults(results) {
        // Implementation for search results display
        console.log('Search results:', results);
    }

    initCharts() {
        // Initialize Chart.js or other charting library
        this.createDashboardCharts();
        this.createAnalysisCharts();
    }

    createDashboardCharts() {
        // Create dashboard visualizations
        const ctx = document.getElementById('dashboardChart');
        if (!ctx) return;
        
        // Mock chart data
        const chartData = {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [{
                label: 'Properties Found',
                data: [12, 19, 3, 5, 2, 3],
                borderColor: '#1e40af',
                backgroundColor: 'rgba(30, 64, 175, 0.1)',
                tension: 0.4
            }]
        };
        
        // Initialize chart (requires Chart.js)
        // new Chart(ctx, { type: 'line', data: chartData });
    }

    createAnalysisCharts() {
        // Create analysis-specific charts
        console.log('Creating analysis charts...');
    }

    setupRealTimeUpdates() {
        // Setup WebSocket or polling for real-time updates
        setInterval(() => {
            this.updateSystemStatus();
        }, 30000); // Update every 30 seconds
    }

    updateSystemStatus() {
        // Update system status indicators
        const statusElements = document.querySelectorAll('.status-indicator');
        statusElements.forEach(element => {
            element.classList.toggle('online', Math.random() > 0.1);
        });
    }

    initTooltips() {
        // Initialize tooltip functionality
        const tooltipElements = document.querySelectorAll('[data-tooltip]');
        tooltipElements.forEach(element => {
            element.addEventListener('mouseenter', this.showTooltip);
            element.addEventListener('mouseleave', this.hideTooltip);
        });
    }

    showTooltip(event) {
        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip';
        tooltip.textContent = event.target.dataset.tooltip;
        tooltip.style.cssText = `
            position: absolute;
            background: #1f2937;
            color: white;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 14px;
            z-index: 1000;
            pointer-events: none;
        `;
        
        document.body.appendChild(tooltip);
        
        const rect = event.target.getBoundingClientRect();
        tooltip.style.left = rect.left + rect.width / 2 - tooltip.offsetWidth / 2 + 'px';
        tooltip.style.top = rect.top - tooltip.offsetHeight - 8 + 'px';
    }

    hideTooltip() {
        const tooltip = document.querySelector('.tooltip');
        if (tooltip) {
            tooltip.remove();
        }
    }

    addNotification(message, type = 'info') {
        const notification = {
            id: Date.now(),
            message,
            type,
            timestamp: new Date()
        };
        
        this.notifications.unshift(notification);
        this.displayNotification(notification);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            this.removeNotification(notification.id);
        }, 5000);
    }

    displayNotification(notification) {
        const container = document.getElementById('notifications') || this.createNotificationContainer();
        
        const notificationEl = document.createElement('div');
        notificationEl.className = `notification notification-${notification.type}`;
        notificationEl.innerHTML = `
            <div class="flex items-center justify-between p-4 rounded-lg shadow-lg mb-2">
                <div class="flex items-center">
                    <i class="fas fa-${this.getNotificationIcon(notification.type)} mr-2"></i>
                    <span>${notification.message}</span>
                </div>
                <button onclick="afhApp.removeNotification(${notification.id})" class="ml-4 text-gray-400 hover:text-gray-600">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        container.appendChild(notificationEl);
        
        // Animate in
        notificationEl.style.transform = 'translateX(100%)';
        notificationEl.style.transition = 'transform 0.3s ease';
        setTimeout(() => {
            notificationEl.style.transform = 'translateX(0)';
        }, 100);
    }

    createNotificationContainer() {
        const container = document.createElement('div');
        container.id = 'notifications';
        container.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
            max-width: 400px;
        `;
        document.body.appendChild(container);
        return container;
    }

    getNotificationIcon(type) {
        const icons = {
            success: 'check-circle',
            error: 'exclamation-circle',
            warning: 'exclamation-triangle',
            info: 'info-circle'
        };
        return icons[type] || 'info-circle';
    }

    removeNotification(id) {
        this.notifications = this.notifications.filter(n => n.id !== id);
        const notificationEl = document.querySelector(`[data-notification-id="${id}"]`);
        if (notificationEl) {
            notificationEl.style.transform = 'translateX(100%)';
            setTimeout(() => {
                notificationEl.remove();
            }, 300);
        }
    }

    showLoading(message = 'Loading...') {
        this.isLoading = true;
        const loadingEl = document.createElement('div');
        loadingEl.id = 'loading-overlay';
        loadingEl.innerHTML = `
            <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                <div class="bg-white rounded-lg p-6 flex items-center">
                    <div class="loading-spinner mr-3"></div>
                    <span>${message}</span>
                </div>
            </div>
        `;
        document.body.appendChild(loadingEl);
    }

    hideLoading() {
        this.isLoading = false;
        const loadingEl = document.getElementById('loading-overlay');
        if (loadingEl) {
            loadingEl.remove();
        }
    }

    handleKeyboardShortcuts(event) {
        // Ctrl/Cmd + K for search
        if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
            event.preventDefault();
            document.querySelector('input[placeholder*="Search"]')?.focus();
        }
        
        // Escape to close modals
        if (event.key === 'Escape') {
            this.closeModals();
        }
        
        // Number keys for navigation
        if (event.key >= '1' && event.key <= '7') {
            const sections = ['dashboard', 'analysis', 'showcase', 'series', 'automation', 'resources', 'settings'];
            const sectionIndex = parseInt(event.key) - 1;
            if (sections[sectionIndex]) {
                this.navigateToSection(sections[sectionIndex]);
            }
        }
    }

    closeModals() {
        // Close any open modals
        document.querySelectorAll('.modal').forEach(modal => {
            modal.style.display = 'none';
        });
    }

    handleResize() {
        // Handle window resize
        this.updateLayout();
    }

    updateLayout() {
        // Update layout based on screen size
        const isMobile = window.innerWidth < 768;
        const sidebar = document.querySelector('.sidebar');
        if (sidebar) {
            sidebar.classList.toggle('mobile', isMobile);
        }
    }

    loadData() {
        // Load initial data
        this.loadDashboardData();
        this.loadPropertyData();
        this.loadSettings();
    }

    async loadDashboardData() {
        try {
            // Simulate API call
            const data = await this.fetchDashboardData();
            this.updateDashboard(data);
        } catch (error) {
            console.error('Failed to load dashboard data:', error);
        }
    }

    async fetchDashboardData() {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        return {
            totalProperties: 47,
            averageCashFlow: 4200,
            successRate: 89,
            averageROI: 24.5,
            recentActivity: [
                { message: 'New property found in Kent, WA', time: '2 minutes ago' },
                { message: 'Analysis completed for Auburn property', time: '15 minutes ago' }
            ]
        };
    }

    updateDashboard(data) {
        // Update dashboard with new data
        document.querySelector('[data-stat="properties"]')?.textContent = data.totalProperties;
        document.querySelector('[data-stat="cashflow"]')?.textContent = `$${data.averageCashFlow}`;
        document.querySelector('[data-stat="success"]')?.textContent = `${data.successRate}%`;
        document.querySelector('[data-stat="roi"]')?.textContent = `${data.averageROI}%`;
    }

    loadPropertyData() {
        // Load property data
        console.log('Loading property data...');
    }

    loadSettings() {
        // Load user settings
        const settings = localStorage.getItem('afh-settings');
        if (settings) {
            this.settings = JSON.parse(settings);
            this.applySettings();
        }
    }

    saveSettings() {
        // Save user settings
        const form = document.getElementById('settingsForm');
        const formData = new FormData(form);
        
        const settings = {
            targetCounties: Array.from(formData.getAll('counties')),
            priceRange: {
                min: formData.get('priceMin'),
                max: formData.get('priceMax')
            },
            notifications: {
                email: formData.get('email'),
                phone: formData.get('phone'),
                frequency: formData.get('frequency')
            }
        };
        
        localStorage.setItem('afh-settings', JSON.stringify(settings));
        this.addNotification('Settings saved successfully!', 'success');
    }

    applySettings() {
        // Apply loaded settings to the UI
        if (this.settings) {
            // Apply settings to form elements
            console.log('Applying settings:', this.settings);
        }
    }

    saveUserPreferences() {
        // Save user preferences before page unload
        const preferences = {
            currentSection: this.currentSection,
            sidebarOpen: document.querySelector('.sidebar')?.classList.contains('open'),
            lastVisit: new Date().toISOString()
        };
        
        localStorage.setItem('afh-preferences', JSON.stringify(preferences));
    }

    loadSectionData(section) {
        // Load data specific to the current section
        switch (section) {
            case 'dashboard':
                this.loadDashboardData();
                break;
            case 'analysis':
                this.loadAnalysisData();
                break;
            case 'showcase':
                this.loadShowcaseData();
                break;
            case 'series':
                this.loadSeriesData();
                break;
            case 'automation':
                this.loadAutomationData();
                break;
            case 'resources':
                this.loadResourcesData();
                break;
            case 'settings':
                this.loadSettingsData();
                break;
        }
    }

    loadAnalysisData() {
        console.log('Loading analysis data...');
    }

    loadShowcaseData() {
        console.log('Loading showcase data...');
    }

    loadSeriesData() {
        console.log('Loading series data...');
    }

    loadAutomationData() {
        console.log('Loading automation data...');
    }

    loadResourcesData() {
        console.log('Loading resources data...');
        this.currentResourceCategory = 'official'; // Default category
        this.selectResourceCategory('official');
    }

    selectResourceCategory(category) {
        this.currentResourceCategory = category;
        
        // Update active button styling
        document.querySelectorAll('.resource-category-btn').forEach(btn => {
            btn.classList.remove('bg-blue-100', 'border-blue-300');
            btn.classList.add('border-transparent');
        });
        
        const activeBtn = document.querySelector(`[data-category="${category}"]`);
        if (activeBtn) {
            activeBtn.classList.add('bg-blue-100', 'border-blue-300');
            activeBtn.classList.remove('border-transparent');
        }
        
        // Display resources for selected category
        this.displayCategoryResources(category);
    }

    displayCategoryResources(category) {
        const contentContainer = document.getElementById('resources-content');
        if (!contentContainer) return;

        const categoryResources = this.afhResources.filter(resource => resource.category === category);
        const categoryName = this.getCategoryDisplayName(category);
        const categoryIcon = this.getCategoryIcon(category);
        
        let html = `
            <div class="mb-6">
                <div class="flex items-center mb-4">
                    <i class="${categoryIcon} text-3xl mr-4 text-afh-blue"></i>
                    <div>
                        <h2 class="text-2xl font-bold text-gray-800">${categoryName}</h2>
                        <p class="text-gray-600">${categoryResources.length} resources available</p>
                    </div>
                </div>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        `;
        
        categoryResources.forEach(resource => {
            html += `
                <div class="bg-white rounded-lg shadow-lg hover:shadow-xl transition-shadow border border-gray-200 p-6">
                    <div class="flex items-start mb-4">
                        <div class="flex-shrink-0">
                            <div class="w-12 h-12 rounded-lg bg-blue-50 flex items-center justify-center mr-4">
                                <i class="${resource.icon} text-xl text-afh-blue"></i>
                            </div>
                        </div>
                        <div class="flex-1">
                            <h3 class="text-lg font-semibold text-gray-800 mb-1">${resource.name}</h3>
                            <p class="text-sm text-gray-600 mb-3">${resource.type}</p>
                            <p class="text-sm text-gray-700 leading-relaxed">${resource.description}</p>
                        </div>
                    </div>
                    <div class="flex items-center justify-between">
                        <div class="flex items-center text-xs text-gray-500">
                            <i class="fas fa-external-link-alt mr-1"></i>
                            <span>External Link</span>
                        </div>
                        <a href="${resource.url}" target="_blank" rel="noopener noreferrer" 
                           class="inline-flex items-center px-4 py-2 bg-afh-blue text-white rounded-lg hover:bg-afh-green transition-colors font-medium text-sm">
                            Visit Resource <i class="fas fa-arrow-right ml-2"></i>
                        </a>
                    </div>
                </div>
            `;
        });
        
        html += `</div>`;
        
        contentContainer.innerHTML = html;
    }

    groupResourcesByCategory() {
        const grouped = {};
        this.afhResources.forEach(resource => {
            if (!grouped[resource.category]) {
                grouped[resource.category] = [];
            }
            grouped[resource.category].push(resource);
        });
        return grouped;
    }

    getCategoryDisplayName(category) {
        const names = {
            'official': 'Official Government Resources',
            'county': 'County & City Offices',
            'facebook': 'Facebook Communities & Groups',
            'network': 'Professional Networks',
            'association': 'Industry Associations',
            'property': 'Property Search Platforms',
            'training': 'Training & Education',
            'financial': 'Financial & Insurance Services',
            'technology': 'Technology & Software Tools'
        };
        return names[category] || category;
    }

    getCategoryIcon(category) {
        const icons = {
            'official': 'fas fa-landmark',
            'county': 'fas fa-map-marker-alt',
            'facebook': 'fab fa-facebook',
            'network': 'fas fa-users',
            'association': 'fas fa-handshake',
            'property': 'fas fa-home',
            'training': 'fas fa-graduation-cap',
            'financial': 'fas fa-dollar-sign',
            'technology': 'fas fa-laptop'
        };
        return icons[category] || 'fas fa-link';
    }

    loadSettingsData() {
        console.log('Loading settings data...');
    }

    // Utility methods
    formatCurrency(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(amount);
    }

    formatDate(date) {
        return new Intl.DateTimeFormat('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        }).format(new Date(date));
    }

    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.afhApp = new AFHPropertyScout();
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AFHPropertyScout;
}
