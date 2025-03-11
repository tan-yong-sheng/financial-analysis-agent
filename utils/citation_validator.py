"""Utility for validating and monitoring citation usage in the system."""

import json
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

def log_source_summary(data: Dict[str, Any], prefix: str = "") -> None:
    """
    Log a summary of source information in the data structure.
    
    Args:
        data: The data to inspect
        prefix: Prefix for log messages
    """
    if isinstance(data, dict):
        # Check for _source field
        if "_source" in data:
            source_info = data["_source"]
            logger.info(f"{prefix}Source found: {source_info.get('name', 'Unknown')}")
            
        # Recursively check all dictionary values
        for key, value in data.items():
            if key != "_source":  # Skip already processed _source field
                log_source_summary(value, f"{prefix}{key}.")
                
    elif isinstance(data, list):
        # Check first few items in the list
        for i, item in enumerate(data[:3]):  # Just check first 3 for brevity
            log_source_summary(item, f"{prefix}[{i}].")

def check_citations_in_analysis(analysis_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Check if citations are present in analysis results.
    
    Args:
        analysis_results: Analysis results to check
        
    Returns:
        Dict with citation stats
    """
    stats = {
        "total_citable_items": 0,
        "items_with_citations": 0,
        "citation_sources": set()
    }
    
    def _check_item(item):
        if isinstance(item, dict) and "content" in item:
            stats["total_citable_items"] += 1
            if "citation" in item and item["citation"]:
                stats["items_with_citations"] += 1
                if item["citation"] != "Internal Analysis":
                    stats["citation_sources"].add(item["citation"])
    
    # Check market trends
    if "analysis" in analysis_results:
        analysis = analysis_results["analysis"]
        
        if "market_trends" in analysis and isinstance(analysis["market_trends"], list):
            for trend in analysis["market_trends"]:
                _check_item(trend)
                
        if "competitive_position" in analysis and isinstance(analysis["competitive_position"], list):
            for item in analysis["competitive_position"]:
                _check_item(item)
                
        if "risks_opportunities" in analysis:
            risks_opps = analysis["risks_opportunities"]
            if "risks" in risks_opps and isinstance(risks_opps["risks"], list):
                for risk in risks_opps["risks"]:
                    _check_item(risk)
            if "opportunities" in risks_opps and isinstance(risks_opps["opportunities"], list):
                for opp in risks_opps["opportunities"]:
                    _check_item(opp)
                    
        if "recent_events" in analysis and isinstance(analysis["recent_events"], list):
            for event in analysis["recent_events"]:
                _check_item(event)
                
        if "industry_outlook" in analysis:
            _check_item(analysis["industry_outlook"])
    
    # Convert set to list for JSON serialization
    stats["citation_sources"] = list(stats["citation_sources"])
    stats["citation_percentage"] = (
        (stats["items_with_citations"] / stats["total_citable_items"] * 100) 
        if stats["total_citable_items"] > 0 else 0
    )
    
    logger.info(f"Citation stats: {stats['items_with_citations']}/{stats['total_citable_items']} items cited ({stats['citation_percentage']:.1f}%)")
    return stats
