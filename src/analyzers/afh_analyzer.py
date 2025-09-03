"""
AFH Financial Analyzer - Analyzes properties for AFH viability and optimal pricing
"""

import math
from typing import Dict, Any, List
from loguru import logger
import pandas as pd

class AFHAnalyzer:
    """Analyzes properties for Adult Family Home financial viability"""
    
    def __init__(self, analysis_config: Dict[str, Any]):
        """Initialize the AFH analyzer with configuration"""
        self.config = analysis_config
        self.medicaid_rate = analysis_config.get('medicaid_rate_per_day', 120)
        self.private_pay_rate = analysis_config.get('private_pay_rate_per_day', 200)
        self.occupancy_rate = analysis_config.get('occupancy_rate', 0.85)
        
        # Monthly operating costs
        self.monthly_utilities = analysis_config.get('utilities', 800)
        self.monthly_insurance = analysis_config.get('insurance', 400)
        self.monthly_maintenance = analysis_config.get('maintenance', 600)
        self.monthly_supplies = analysis_config.get('supplies', 500)
        self.monthly_licensing = analysis_config.get('licensing_fees', 200)
        
        # Target metrics
        self.min_cash_flow = analysis_config.get('min_cash_flow', 3000)
        self.min_cap_rate = analysis_config.get('min_cap_rate', 0.08)
        self.max_debt_ratio = analysis_config.get('max_debt_ratio', 0.75)
    
    def analyze_property(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a property for AFH viability and return comprehensive analysis"""
        try:
            logger.info(f"Analyzing property: {property_data.get('address', 'Unknown')}")
            
            # Basic property analysis
            basic_analysis = self._analyze_basic_viability(property_data)
            
            # Financial analysis
            financial_analysis = self._analyze_financials(property_data)
            
            # Market analysis
            market_analysis = self._analyze_market_position(property_data)
            
            # WABO and licensing analysis
            wabo_analysis = self._analyze_wabo_status(property_data)
            
            # Risk assessment
            risk_analysis = self._assess_risks(property_data)
            
            # Optimal pricing analysis
            pricing_analysis = self._calculate_optimal_pricing(property_data, financial_analysis)
            
            # Overall viability score
            viability_score = self._calculate_viability_score(
                basic_analysis, financial_analysis, market_analysis, 
                wabo_analysis, risk_analysis
            )
            
            # Compile final analysis
            analysis = {
                'viable': viability_score >= 70,  # 70% threshold for viability
                'viability_score': viability_score,
                'basic_analysis': basic_analysis,
                'financial_analysis': financial_analysis,
                'market_analysis': market_analysis,
                'wabo_analysis': wabo_analysis,
                'risk_analysis': risk_analysis,
                'pricing_analysis': pricing_analysis,
                'recommendations': self._generate_recommendations(
                    basic_analysis, financial_analysis, market_analysis,
                    wabo_analysis, risk_analysis, pricing_analysis
                ),
                'analysis_date': pd.Timestamp.now().isoformat()
            }
            
            logger.info(f"Analysis completed. Viability: {viability_score:.1f}%")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing property: {e}")
            return {
                'viable': False,
                'viability_score': 0,
                'error': str(e),
                'analysis_date': pd.Timestamp.now().isoformat()
            }
    
    def _analyze_basic_viability(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze basic property characteristics for AFH suitability"""
        score = 0
        max_score = 100
        issues = []
        strengths = []
        
        # Check bedrooms (need at least 3, prefer 4+)
        bedrooms = property_data.get('bedrooms', 0)
        if bedrooms >= 4:
            score += 25
            strengths.append(f"Excellent: {bedrooms} bedrooms")
        elif bedrooms >= 3:
            score += 15
            strengths.append(f"Good: {bedrooms} bedrooms")
        else:
            score += 0
            issues.append(f"Insufficient bedrooms: {bedrooms}")
        
        # Check bathrooms (need at least 2, prefer 3+)
        bathrooms = property_data.get('bathrooms', 0)
        if bathrooms >= 3:
            score += 20
            strengths.append(f"Excellent: {bathrooms} bathrooms")
        elif bathrooms >= 2:
            score += 15
            strengths.append(f"Good: {bathrooms} bathrooms")
        else:
            score += 0
            issues.append(f"Insufficient bathrooms: {bathrooms}")
        
        # Check square footage (need 2000+, prefer 2500+)
        sqft = property_data.get('sqft', 0)
        if sqft >= 2500:
            score += 20
            strengths.append(f"Excellent: {sqft:,} sqft")
        elif sqft >= 2000:
            score += 15
            strengths.append(f"Good: {sqft:,} sqft")
        else:
            score += 0
            issues.append(f"Insufficient square footage: {sqft:,} sqft")
        
        # Check property type (prefer rambler/single story)
        property_type = property_data.get('property_type', '').lower()
        if 'rambler' in property_type or 'single story' in property_type:
            score += 15
            strengths.append("Single story - ideal for AFH")
        elif 'two story' in property_type or 'multi' in property_type:
            score += 5
            issues.append("Multi-story may require modifications")
        else:
            score += 10  # Neutral
        
        # Check county (target counties get bonus)
        county = property_data.get('county', '').lower()
        target_counties = ['lewis', 'thurston', 'pierce', 'king']
        if any(target in county for target in target_counties):
            score += 10
            strengths.append(f"Target county: {county}")
        else:
            score += 5  # Still acceptable
        
        # Check price range
        price = property_data.get('price', 0)
        if 300000 <= price <= 1500000:
            score += 10
            strengths.append(f"Price in target range: ${price:,.0f}")
        elif price > 1500000:
            score += 0
            issues.append(f"Price may be too high: ${price:,.0f}")
        else:
            score += 5
            issues.append(f"Price may be too low: ${price:,.0f}")
        
        return {
            'score': score,
            'max_score': max_score,
            'percentage': (score / max_score) * 100,
            'issues': issues,
            'strengths': strengths
        }
    
    def _analyze_financials(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze financial viability of the property"""
        price = property_data.get('price', 0)
        bedrooms = property_data.get('bedrooms', 0)
        
        # Calculate potential revenue
        # Assume mix of Medicaid and private pay residents
        medicaid_residents = math.floor(bedrooms * 0.6)  # 60% Medicaid
        private_residents = bedrooms - medicaid_residents  # 40% private pay
        
        monthly_medicaid_revenue = medicaid_residents * self.medicaid_rate * 30 * self.occupancy_rate
        monthly_private_revenue = private_residents * self.private_pay_rate * 30 * self.occupancy_rate
        total_monthly_revenue = monthly_medicaid_revenue + monthly_private_revenue
        
        # Calculate operating expenses
        total_monthly_expenses = (
            self.monthly_utilities + self.monthly_insurance + 
            self.monthly_maintenance + self.monthly_supplies + self.monthly_licensing
        )
        
        # Calculate debt service (assuming 80% LTV, 6% interest, 30-year term)
        loan_amount = price * 0.8
        monthly_interest_rate = 0.06 / 12
        num_payments = 30 * 12
        monthly_payment = loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate)**num_payments) / ((1 + monthly_interest_rate)**num_payments - 1)
        
        # Calculate cash flow
        monthly_cash_flow = total_monthly_revenue - total_monthly_expenses - monthly_payment
        
        # Calculate cap rate
        annual_net_income = (total_monthly_revenue - total_monthly_expenses) * 12
        cap_rate = annual_net_income / price if price > 0 else 0
        
        # Calculate debt service coverage ratio
        dscr = (total_monthly_revenue - total_monthly_expenses) / monthly_payment if monthly_payment > 0 else 0
        
        return {
            'purchase_price': price,
            'loan_amount': loan_amount,
            'monthly_payment': monthly_payment,
            'monthly_revenue': {
                'medicaid': monthly_medicaid_revenue,
                'private_pay': monthly_private_revenue,
                'total': total_monthly_revenue
            },
            'monthly_expenses': total_monthly_expenses,
            'monthly_cash_flow': monthly_cash_flow,
            'annual_cash_flow': monthly_cash_flow * 12,
            'cap_rate': cap_rate,
            'dscr': dscr,
            'occupancy_assumption': self.occupancy_rate,
            'resident_mix': {
                'medicaid': medicaid_residents,
                'private_pay': private_residents,
                'total': bedrooms
            }
        }
    
    def _analyze_market_position(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze market position and competitiveness"""
        price = property_data.get('price', 0)
        sqft = property_data.get('sqft', 0)
        county = property_data.get('county', '').lower()
        
        # Price per square foot
        price_per_sqft = price / sqft if sqft > 0 else 0
        
        # Market positioning based on county
        county_analysis = {
            'king': {'avg_price_per_sqft': 400, 'market_demand': 'high', 'competition': 'high'},
            'pierce': {'avg_price_per_sqft': 250, 'market_demand': 'medium', 'competition': 'medium'},
            'thurston': {'avg_price_per_sqft': 200, 'market_demand': 'medium', 'competition': 'low'},
            'lewis': {'avg_price_per_sqft': 150, 'market_demand': 'low', 'competition': 'low'}
        }
        
        market_data = None
        for county_key, data in county_analysis.items():
            if county_key in county:
                market_data = data
                break
        
        if not market_data:
            market_data = {'avg_price_per_sqft': 250, 'market_demand': 'medium', 'competition': 'medium'}
        
        # Compare to market average
        market_comparison = 'at_market'
        if price_per_sqft < market_data['avg_price_per_sqft'] * 0.9:
            market_comparison = 'below_market'
        elif price_per_sqft > market_data['avg_price_per_sqft'] * 1.1:
            market_comparison = 'above_market'
        
        return {
            'price_per_sqft': price_per_sqft,
            'market_avg_price_per_sqft': market_data['avg_price_per_sqft'],
            'market_comparison': market_comparison,
            'market_demand': market_data['market_demand'],
            'competition_level': market_data['competition'],
            'county': county
        }
    
    def _analyze_wabo_status(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze WABO status and licensing readiness"""
        wabo_status = property_data.get('wabo_status', 'unknown')
        description = property_data.get('description', '').lower()
        
        # WABO status scoring
        wabo_scores = {
            'approved': 100,
            'inspected': 80,
            'mentioned': 60,
            'none': 20,
            'unknown': 30
        }
        
        wabo_score = wabo_scores.get(wabo_status, 30)
        
        # Additional WABO-related keywords
        wabo_keywords = {
            'dshs': 20,
            'licensed': 25,
            'inspection': 15,
            'ready': 20,
            'turnkey': 15,
            'renovated': 10
        }
        
        keyword_bonus = 0
        for keyword, bonus in wabo_keywords.items():
            if keyword in description:
                keyword_bonus += bonus
        
        total_wabo_score = min(wabo_score + keyword_bonus, 100)
        
        # Estimate licensing timeline and costs
        if wabo_status == 'approved':
            licensing_timeline = '1-3 months'
            estimated_licensing_cost = 5000
        elif wabo_status == 'inspected':
            licensing_timeline = '3-6 months'
            estimated_licensing_cost = 10000
        else:
            licensing_timeline = '6-12 months'
            estimated_licensing_cost = 20000
        
        return {
            'wabo_status': wabo_status,
            'wabo_score': total_wabo_score,
            'licensing_timeline': licensing_timeline,
            'estimated_licensing_cost': estimated_licensing_cost,
            'keyword_bonus': keyword_bonus,
            'description_analysis': description
        }
    
    def _assess_risks(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess various risks associated with the property"""
        risks = []
        risk_score = 0
        
        # Price risk
        price = property_data.get('price', 0)
        if price > 1200000:
            risks.append('High purchase price may limit financing options')
            risk_score += 20
        elif price < 400000:
            risks.append('Low price may indicate property issues')
            risk_score += 15
        
        # Location risk
        county = property_data.get('county', '').lower()
        if 'lewis' in county:
            risks.append('Lewis County has lower demand and longer licensing times')
            risk_score += 10
        
        # Property condition risk
        description = property_data.get('description', '').lower()
        if 'needs work' in description or 'fixer' in description:
            risks.append('Property may require significant renovations')
            risk_score += 25
        elif 'turnkey' in description or 'renovated' in description:
            risk_score -= 10  # Reduce risk
        
        # WABO risk
        wabo_status = property_data.get('wabo_status', 'unknown')
        if wabo_status == 'none':
            risks.append('No WABO approval - significant licensing risk')
            risk_score += 30
        elif wabo_status == 'unknown':
            risks.append('Unknown WABO status - verification needed')
            risk_score += 15
        
        # Market risk
        sqft = property_data.get('sqft', 0)
        if sqft < 2200:
            risks.append('Smaller property may limit resident capacity')
            risk_score += 10
        
        return {
            'total_risk_score': max(0, min(100, risk_score)),
            'risks': risks,
            'risk_level': 'low' if risk_score < 30 else 'medium' if risk_score < 60 else 'high'
        }
    
    def _calculate_optimal_pricing(self, property_data: Dict[str, Any], financial_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate optimal purchase price for successful AFH operation"""
        current_price = property_data.get('price', 0)
        
        # Calculate maximum price based on cash flow requirements
        monthly_cash_flow_target = self.min_cash_flow
        monthly_revenue = financial_analysis['monthly_revenue']['total']
        monthly_expenses = financial_analysis['monthly_expenses']
        
        # Maximum monthly payment that still meets cash flow target
        max_monthly_payment = monthly_revenue - monthly_expenses - monthly_cash_flow_target
        
        # Calculate maximum loan amount from monthly payment
        monthly_interest_rate = 0.06 / 12
        num_payments = 30 * 12
        if max_monthly_payment > 0:
            max_loan_amount = max_monthly_payment * ((1 + monthly_interest_rate)**num_payments - 1) / (monthly_interest_rate * (1 + monthly_interest_rate)**num_payments)
            max_purchase_price = max_loan_amount / 0.8  # 80% LTV
        else:
            max_purchase_price = 0
        
        # Calculate price based on cap rate
        annual_net_income = (monthly_revenue - monthly_expenses) * 12
        cap_rate_price = annual_net_income / self.min_cap_rate if self.min_cap_rate > 0 else 0
        
        # Take the lower of the two calculations
        optimal_price = min(max_purchase_price, cap_rate_price) if max_purchase_price > 0 and cap_rate_price > 0 else max(max_purchase_price, cap_rate_price)
        
        # Negotiation strategy
        negotiation_strategy = self._generate_negotiation_strategy(current_price, optimal_price, property_data)
        
        return {
            'current_price': current_price,
            'optimal_price': optimal_price,
            'max_price': max_purchase_price,
            'cap_rate_price': cap_rate_price,
            'negotiation_target': optimal_price * 0.95,  # 5% below optimal
            'negotiation_strategy': negotiation_strategy,
            'price_difference': current_price - optimal_price,
            'price_difference_percentage': ((current_price - optimal_price) / current_price * 100) if current_price > 0 else 0
        }
    
    def _generate_negotiation_strategy(self, current_price: float, optimal_price: float, property_data: Dict[str, Any]) -> List[str]:
        """Generate negotiation strategy and tactics"""
        strategies = []
        
        if current_price > optimal_price:
            price_diff = current_price - optimal_price
            price_diff_pct = (price_diff / current_price) * 100
            
            if price_diff_pct > 20:
                strategies.append("Property significantly overpriced - consider walking away")
            elif price_diff_pct > 10:
                strategies.append("Strong negotiation position - target 15-20% reduction")
            else:
                strategies.append("Moderate negotiation needed - target 5-10% reduction")
            
            # Specific negotiation points
            wabo_status = property_data.get('wabo_status', 'unknown')
            if wabo_status == 'none':
                strategies.append("Use lack of WABO approval as major negotiation point")
                strategies.append("Request 20-30% reduction for licensing uncertainty")
            
            if 'needs work' in property_data.get('description', '').lower():
                strategies.append("Use renovation needs as negotiation leverage")
                strategies.append("Request inspection contingency")
            
            strategies.append("Emphasize cash offer and quick closing")
            strategies.append("Highlight specialized use case (AFH) limiting buyer pool")
            
        else:
            strategies.append("Property priced reasonably - consider full price offer")
            strategies.append("Emphasize quick closing and cash offer")
            strategies.append("Highlight serious buyer status")
        
        return strategies
    
    def _calculate_viability_score(self, basic_analysis: Dict, financial_analysis: Dict, 
                                 market_analysis: Dict, wabo_analysis: Dict, risk_analysis: Dict) -> float:
        """Calculate overall viability score"""
        # Weighted scoring
        weights = {
            'basic': 0.25,      # 25% - Property characteristics
            'financial': 0.30,  # 30% - Financial viability
            'market': 0.15,     # 15% - Market position
            'wabo': 0.20,       # 20% - WABO status
            'risk': 0.10        # 10% - Risk assessment
        }
        
        # Calculate weighted score
        basic_score = basic_analysis['percentage']
        financial_score = self._calculate_financial_score(financial_analysis)
        market_score = self._calculate_market_score(market_analysis)
        wabo_score = wabo_analysis['wabo_score']
        risk_score = 100 - risk_analysis['total_risk_score']  # Invert risk score
        
        total_score = (
            basic_score * weights['basic'] +
            financial_score * weights['financial'] +
            market_score * weights['market'] +
            wabo_score * weights['wabo'] +
            risk_score * weights['risk']
        )
        
        return total_score
    
    def _calculate_financial_score(self, financial_analysis: Dict) -> float:
        """Calculate financial viability score"""
        score = 0
        
        # Cash flow score
        monthly_cash_flow = financial_analysis['monthly_cash_flow']
        if monthly_cash_flow >= self.min_cash_flow * 1.5:
            score += 40
        elif monthly_cash_flow >= self.min_cash_flow:
            score += 30
        elif monthly_cash_flow >= self.min_cash_flow * 0.5:
            score += 20
        else:
            score += 0
        
        # Cap rate score
        cap_rate = financial_analysis['cap_rate']
        if cap_rate >= self.min_cap_rate * 1.2:
            score += 30
        elif cap_rate >= self.min_cap_rate:
            score += 25
        elif cap_rate >= self.min_cap_rate * 0.8:
            score += 15
        else:
            score += 0
        
        # DSCR score
        dscr = financial_analysis['dscr']
        if dscr >= 1.5:
            score += 30
        elif dscr >= 1.25:
            score += 25
        elif dscr >= 1.0:
            score += 20
        else:
            score += 0
        
        return min(score, 100)
    
    def _calculate_market_score(self, market_analysis: Dict) -> float:
        """Calculate market position score"""
        score = 50  # Base score
        
        # Market comparison
        comparison = market_analysis['market_comparison']
        if comparison == 'below_market':
            score += 30
        elif comparison == 'at_market':
            score += 20
        else:  # above_market
            score += 0
        
        # Market demand
        demand = market_analysis['market_demand']
        if demand == 'high':
            score += 20
        elif demand == 'medium':
            score += 10
        else:  # low
            score += 0
        
        return min(score, 100)
    
    def _generate_recommendations(self, basic_analysis: Dict, financial_analysis: Dict,
                                market_analysis: Dict, wabo_analysis: Dict, 
                                risk_analysis: Dict, pricing_analysis: Dict) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Basic recommendations
        if basic_analysis['percentage'] < 70:
            recommendations.append("Property may need modifications to meet AFH requirements")
        
        # Financial recommendations
        if financial_analysis['monthly_cash_flow'] < self.min_cash_flow:
            recommendations.append("Consider negotiating price down to improve cash flow")
            recommendations.append("Evaluate financing options for better terms")
        
        # WABO recommendations
        if wabo_analysis['wabo_status'] == 'none':
            recommendations.append("Budget for WABO inspection and modifications")
            recommendations.append("Contact DSHS for licensing timeline and requirements")
        elif wabo_analysis['wabo_status'] == 'unknown':
            recommendations.append("Verify WABO status before making offer")
        
        # Risk recommendations
        if risk_analysis['risk_level'] == 'high':
            recommendations.append("Conduct thorough property inspection")
            recommendations.append("Consider professional property evaluation")
        
        # Pricing recommendations
        if pricing_analysis['current_price'] > pricing_analysis['optimal_price']:
            recommendations.append(f"Target negotiation price: ${pricing_analysis['negotiation_target']:,.0f}")
            recommendations.append("Use AFH-specific factors in negotiation")
        
        return recommendations
