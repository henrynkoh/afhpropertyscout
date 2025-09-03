"""
Property Filter - Filters properties based on AFH criteria
"""

from typing import List, Dict, Any
from loguru import logger
import re

class PropertyFilter:
    """Filters properties based on AFH-specific criteria"""
    
    def __init__(self, criteria_config: Dict[str, Any]):
        """Initialize property filter with criteria configuration"""
        self.criteria = criteria_config
        self.target_counties = [county.lower() for county in criteria_config.get('target_counties', [])]
        self.min_bedrooms = criteria_config.get('min_bedrooms', 3)
        self.min_bathrooms = criteria_config.get('min_bathrooms', 2)
        self.min_sqft = criteria_config.get('min_sqft', 2000)
        self.max_price = criteria_config.get('max_price', 1500000)
        self.min_price = criteria_config.get('min_price', 300000)
        self.property_type = criteria_config.get('property_type', '1st floor rambler')
    
    def filter_properties(self, properties: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter properties based on AFH criteria"""
        logger.info(f"Filtering {len(properties)} properties based on AFH criteria")
        
        filtered_properties = []
        
        for property_data in properties:
            try:
                if self._meets_criteria(property_data):
                    filtered_properties.append(property_data)
                else:
                    logger.debug(f"Property filtered out: {property_data.get('address', 'Unknown')}")
            except Exception as e:
                logger.warning(f"Error filtering property: {e}")
                continue
        
        logger.info(f"Filtered to {len(filtered_properties)} properties meeting criteria")
        return filtered_properties
    
    def _meets_criteria(self, property_data: Dict[str, Any]) -> bool:
        """Check if property meets all AFH criteria"""
        # Check county
        if not self._meets_county_criteria(property_data):
            return False
        
        # Check bedrooms
        if not self._meets_bedroom_criteria(property_data):
            return False
        
        # Check bathrooms
        if not self._meets_bathroom_criteria(property_data):
            return False
        
        # Check square footage
        if not self._meets_sqft_criteria(property_data):
            return False
        
        # Check price range
        if not self._meets_price_criteria(property_data):
            return False
        
        # Check property type
        if not self._meets_property_type_criteria(property_data):
            return False
        
        # Check for AFH-related keywords (bonus points)
        if not self._has_afh_potential(property_data):
            return False
        
        return True
    
    def _meets_county_criteria(self, property_data: Dict[str, Any]) -> bool:
        """Check if property is in target county"""
        county = property_data.get('county', '').lower()
        city = property_data.get('city', '').lower()
        
        # Check if county matches target counties
        for target_county in self.target_counties:
            if target_county in county:
                return True
        
        # Check if city is in target counties (fallback)
        target_cities = {
            'lewis': ['centralia', 'chehalis', 'morton', 'packwood'],
            'thurston': ['olympia', 'lacey', 'tumwater', 'yelm'],
            'pierce': ['tacoma', 'puyallup', 'lakewood', 'university place', 'federal way', 'auburn', 'kent', 'renton'],
            'king': ['seattle', 'bellevue', 'kirkland', 'redmond', 'renton', 'kent', 'auburn', 'federal way', 'bothell', 'lynnwood', 'mountlake terrace']
        }
        
        for county_key, cities in target_cities.items():
            if any(city_name in city for city_name in cities):
                return True
        
        return False
    
    def _meets_bedroom_criteria(self, property_data: Dict[str, Any]) -> bool:
        """Check if property meets bedroom criteria"""
        bedrooms = property_data.get('bedrooms', 0)
        return bedrooms >= self.min_bedrooms
    
    def _meets_bathroom_criteria(self, property_data: Dict[str, Any]) -> bool:
        """Check if property meets bathroom criteria"""
        bathrooms = property_data.get('bathrooms', 0)
        return bathrooms >= self.min_bathrooms
    
    def _meets_sqft_criteria(self, property_data: Dict[str, Any]) -> bool:
        """Check if property meets square footage criteria"""
        sqft = property_data.get('sqft', 0)
        return sqft >= self.min_sqft
    
    def _meets_price_criteria(self, property_data: Dict[str, Any]) -> bool:
        """Check if property meets price criteria"""
        price = property_data.get('price', 0)
        return self.min_price <= price <= self.max_price
    
    def _meets_property_type_criteria(self, property_data: Dict[str, Any]) -> bool:
        """Check if property meets property type criteria"""
        property_type = property_data.get('property_type', '').lower()
        description = property_data.get('description', '').lower()
        
        # Look for rambler/single story indicators
        rambler_indicators = [
            'rambler', 'single story', 'one story', '1 story', 'ranch',
            'single level', 'one level', '1 level'
        ]
        
        # Check property type field
        if any(indicator in property_type for indicator in rambler_indicators):
            return True
        
        # Check description field
        if any(indicator in description for indicator in rambler_indicators):
            return True
        
        # If no specific type mentioned, assume it could be suitable
        # (we'll let the analysis determine if it's actually suitable)
        return True
    
    def _has_afh_potential(self, property_data: Dict[str, Any]) -> bool:
        """Check if property has AFH potential based on keywords and characteristics"""
        description = property_data.get('description', '').lower()
        address = property_data.get('address', '').lower()
        
        # AFH-related keywords that indicate potential
        afh_keywords = [
            'adult family home', 'afh', 'wabo', 'dshs', 'licensed',
            'care facility', 'assisted living', 'elderly care',
            'rambler', 'single story', 'accessible', 'wheelchair',
            'large lot', 'quiet neighborhood', 'residential care'
        ]
        
        # Check for AFH-related keywords
        if any(keyword in description for keyword in afh_keywords):
            return True
        
        # Check for characteristics that make it suitable for AFH
        suitable_characteristics = [
            'large', 'spacious', 'open floor plan', 'main floor',
            'ground level', 'no stairs', 'level entry'
        ]
        
        if any(char in description for char in suitable_characteristics):
            return True
        
        # If no specific indicators, still consider it (let analysis decide)
        return True
    
    def get_filter_summary(self, properties: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get summary of filtering results"""
        total_properties = len(properties)
        
        # Count by county
        county_counts = {}
        for prop in properties:
            county = prop.get('county', 'Unknown')
            county_counts[county] = county_counts.get(county, 0) + 1
        
        # Count by price range
        price_ranges = {
            'under_500k': 0,
            '500k_750k': 0,
            '750k_1m': 0,
            '1m_1.5m': 0,
            'over_1.5m': 0
        }
        
        for prop in properties:
            price = prop.get('price', 0)
            if price < 500000:
                price_ranges['under_500k'] += 1
            elif price < 750000:
                price_ranges['500k_750k'] += 1
            elif price < 1000000:
                price_ranges['750k_1m'] += 1
            elif price < 1500000:
                price_ranges['1m_1.5m'] += 1
            else:
                price_ranges['over_1.5m'] += 1
        
        # Count by WABO status
        wabo_counts = {}
        for prop in properties:
            wabo_status = prop.get('wabo_status', 'unknown')
            wabo_counts[wabo_status] = wabo_counts.get(wabo_status, 0) + 1
        
        return {
            'total_properties': total_properties,
            'county_distribution': county_counts,
            'price_distribution': price_ranges,
            'wabo_status_distribution': wabo_counts,
            'criteria_used': {
                'target_counties': self.target_counties,
                'min_bedrooms': self.min_bedrooms,
                'min_bathrooms': self.min_bathrooms,
                'min_sqft': self.min_sqft,
                'price_range': f"${self.min_price:,} - ${self.max_price:,}",
                'property_type': self.property_type
            }
        }
    
    def create_filtered_report(self, properties: List[Dict[str, Any]]) -> str:
        """Create a detailed report of filtered properties"""
        if not properties:
            return "No properties found matching the criteria."
        
        report = f"""
AFH Property Filter Report
========================

Total Properties Found: {len(properties)}

Filter Criteria:
- Target Counties: {', '.join(self.target_counties)}
- Minimum Bedrooms: {self.min_bedrooms}
- Minimum Bathrooms: {self.min_bathrooms}
- Minimum Square Feet: {self.min_sqft:,}
- Price Range: ${self.min_price:,} - ${self.max_price:,}
- Property Type: {self.property_type}

Property Details:
"""
        
        for i, prop in enumerate(properties, 1):
            report += f"""
{i}. {prop.get('address', 'Unknown Address')}
   Price: ${prop.get('price', 0):,.0f}
   Beds/Baths: {prop.get('bedrooms', 0)}/{prop.get('bathrooms', 0)}
   Square Feet: {prop.get('sqft', 0):,}
   County: {prop.get('county', 'Unknown')}
   WABO Status: {prop.get('wabo_status', 'Unknown')}
   Source: {prop.get('source', 'Unknown')}
   URL: {prop.get('url', 'No URL')}
"""
        
        return report
