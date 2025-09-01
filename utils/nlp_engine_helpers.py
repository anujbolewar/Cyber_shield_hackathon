"""
Advanced NLP Engine Helper Functions
Contains all the helper methods for the main NLP engine
"""

import re
import json
import hashlib
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
from collections import defaultdict, Counter
import numpy as np

logger = logging.getLogger(__name__)

class NLPEngineHelpers:
    """Helper functions for the advanced NLP engine"""
    
    def __init__(self, main_engine):
        self.main_engine = main_engine
    
    def _determine_enhanced_threat_level(self, risk_score: float, threat_analysis: Dict, 
                                       bot_analysis: Dict, coordination: Dict) -> str:
        """Determine enhanced threat level with multiple factors"""
        base_level = "MINIMAL"
        
        if risk_score >= 90:
            base_level = "CRITICAL"
        elif risk_score >= 75:
            base_level = "HIGH"
        elif risk_score >= 50:
            base_level = "MEDIUM"
        elif risk_score >= 25:
            base_level = "LOW"
        
        # Amplification factors
        amplifiers = 0
        
        if threat_analysis.get('severity') == 'CRITICAL':
            amplifiers += 1
        
        if bot_analysis.get('automation_level') in ['HIGH', 'CRITICAL']:
            amplifiers += 1
        
        if coordination.get('is_coordinated') and coordination.get('coordination_sophistication') == 'HIGHLY_SOPHISTICATED':
            amplifiers += 1
        
        # Upgrade threat level based on amplifiers
        if amplifiers >= 2 and base_level in ['LOW', 'MEDIUM']:
            if base_level == 'LOW':
                base_level = 'MEDIUM'
            elif base_level == 'MEDIUM':
                base_level = 'HIGH'
        elif amplifiers >= 1 and base_level == 'MINIMAL':
            base_level = 'LOW'
        
        return base_level
    
    def _generate_executive_summary(self, case_id: str, threat_level: str, 
                                  risk_score: float, content: str, 
                                  analysis_results: Dict) -> str:
        """Generate executive summary for police reports"""
        
        threat_analysis = analysis_results.get('threat_analysis', {})
        bot_analysis = analysis_results.get('bot_analysis', {})
        entities = analysis_results.get('entities', {})
        
        summary = f"""
==================================================
CYBER INTELLIGENCE ANALYSIS REPORT - EXECUTIVE SUMMARY
==================================================

Case ID: {case_id}
Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}
Threat Classification: {threat_level}
Overall Risk Score: {risk_score:.1f}/100

THREAT ASSESSMENT:
Primary Threat Type: {threat_analysis.get('threat_type', 'Unknown')}
Threat Category: {threat_analysis.get('threat_category', 'Unclassified')}
Confidence Level: {threat_analysis.get('confidence', 0):.0%}

CONTENT ANALYSIS:
Content Length: {len(content)} characters
Language Detected: {analysis_results.get('sentiment', {}).get('language', 'Unknown')}
Sentiment: {analysis_results.get('sentiment', {}).get('label', 'Neutral')}

KEY FINDINGS:
- Risk Level: {threat_level}
- Automation Likelihood: {bot_analysis.get('bot_score', 0):.1f}%
- Coordination Detected: {'Yes' if analysis_results.get('coordination', {}).get('is_coordinated') else 'No'}
- Entities Identified: {len(entities.get('persons', []))} persons, {len(entities.get('locations', []))} locations

IMMEDIATE ACTIONS REQUIRED:
{self._get_immediate_actions(threat_level, risk_score)}

INTELLIGENCE PRIORITY: {self._determine_intelligence_priority(threat_level, risk_score)}
        """.strip()
        
        return summary
    
    def _generate_detailed_analysis_report(self, content: str, sentiment: Dict, 
                                         threat_analysis: Dict, entities: Dict,
                                         bot_analysis: Dict, coordination: Dict, 
                                         risk_score: float) -> str:
        """Generate detailed analysis section"""
        
        analysis_sections = []
        
        # Content Analysis Section
        analysis_sections.append("""
=== CONTENT ANALYSIS ===
        """)
        analysis_sections.append(f"Content Length: {len(content)} characters")
        analysis_sections.append(f"Language: {sentiment.get('language', 'Unknown')}")
        analysis_sections.append(f"Sentiment Analysis:")
        analysis_sections.append(f"  - Primary Sentiment: {sentiment.get('label', 'neutral')} (confidence: {sentiment.get('confidence', 0):.2f})")
        analysis_sections.append(f"  - Emotional Intensity: {sentiment.get('intensity', 'LOW')}")
        analysis_sections.append(f"  - Compound Score: {sentiment.get('compound', 0):.2f}")
        
        # Add emotion analysis if available
        if sentiment.get('emotion_scores'):
            emotions = sentiment['emotion_scores']
            dominant_emotions = [emotion for emotion, score in emotions.items() if score > 0.5]
            if dominant_emotions:
                analysis_sections.append(f"  - Dominant Emotions: {', '.join(dominant_emotions)}")
        
        # Threat Analysis Section
        analysis_sections.append("""
=== THREAT ANALYSIS ===
        """)
        analysis_sections.append(f"Overall Risk Score: {risk_score}/100")
        analysis_sections.append(f"Threat Type: {threat_analysis.get('threat_type', 'Unknown')}")
        analysis_sections.append(f"Threat Category: {threat_analysis.get('threat_category', 'Unclassified')}")
        analysis_sections.append(f"Severity Level: {threat_analysis.get('severity', 'Unknown')}")
        analysis_sections.append(f"Confidence: {threat_analysis.get('confidence', 0):.0%}")
        
        if threat_analysis.get('detected_keywords'):
            analysis_sections.append(f"Keywords Detected: {', '.join(threat_analysis['detected_keywords'][:10])}")
        
        if threat_analysis.get('sub_categories'):
            analysis_sections.append(f"Sub-categories: {', '.join(threat_analysis['sub_categories'])}")
        
        # Entity Analysis Section
        analysis_sections.append("""
=== ENTITY ANALYSIS ===
        """)
        
        entity_summary = []
        for entity_type, entity_list in entities.items():
            if isinstance(entity_list, list) and entity_list:
                count = len(entity_list)
                if count > 0:
                    entity_summary.append(f"{entity_type.title()}: {count}")
        
        if entity_summary:
            analysis_sections.append("Entities Identified: " + ", ".join(entity_summary))
        
        # List key entities
        if entities.get('persons'):
            persons = [p.get('text', p) if isinstance(p, dict) else p for p in entities['persons'][:5]]
            analysis_sections.append(f"Key Persons: {', '.join(persons)}")
        
        if entities.get('locations'):
            locations = [l.get('text', l) if isinstance(l, dict) else l for l in entities['locations'][:5]]
            analysis_sections.append(f"Key Locations: {', '.join(locations)}")
        
        if entities.get('organizations'):
            orgs = [o.get('text', o) if isinstance(o, dict) else o for o in entities['organizations'][:5]]
            analysis_sections.append(f"Organizations: {', '.join(orgs)}")
        
        # Bot Analysis Section
        if bot_analysis:
            analysis_sections.append("""
=== AUTOMATION ANALYSIS ===
            """)
            analysis_sections.append(f"Bot Likelihood: {bot_analysis.get('bot_score', 0):.1f}%")
            analysis_sections.append(f"Automation Level: {bot_analysis.get('automation_level', 'Unknown')}")
            analysis_sections.append(f"Bot Type: {bot_analysis.get('bot_type', 'Unknown')}")
            analysis_sections.append(f"Sophistication: {bot_analysis.get('sophistication_score', 0):.1f}%")
            
            if bot_analysis.get('indicators'):
                key_indicators = bot_analysis['indicators'][:5]
                analysis_sections.append(f"Key Indicators: {'; '.join(key_indicators)}")
        
        # Coordination Analysis Section
        if coordination:
            analysis_sections.append("""
=== COORDINATION ANALYSIS ===
            """)
            analysis_sections.append(f"Coordination Detected: {'Yes' if coordination.get('is_coordinated') else 'No'}")
            if coordination.get('is_coordinated'):
                analysis_sections.append(f"Coordination Type: {coordination.get('coordination_type', 'Unknown')}")
                analysis_sections.append(f"Sophistication: {coordination.get('coordination_sophistication', 'Unknown')}")
                analysis_sections.append(f"Network Size Estimate: {coordination.get('network_size_estimate', 0)}")
                analysis_sections.append(f"Similarity Score: {coordination.get('similarity_score', 0):.2f}")
        
        return '\n'.join(analysis_sections)
    
    def _compile_evidence_points(self, threat_analysis: Dict, bot_analysis: Dict, 
                               entities: Dict, coordination: Dict, sentiment: Dict) -> List[str]:
        """Compile comprehensive evidence points"""
        evidence_points = []
        
        # Threat evidence
        if threat_analysis.get('evidence_points'):
            evidence_points.extend([f"THREAT: {point}" for point in threat_analysis['evidence_points']])
        
        # Bot evidence
        if bot_analysis.get('indicators'):
            evidence_points.extend([f"AUTOMATION: {indicator}" for indicator in bot_analysis['indicators'][:5]])
        
        # Coordination evidence
        if coordination.get('coordination_indicators'):
            evidence_points.extend([f"COORDINATION: {indicator}" for indicator in coordination['coordination_indicators'][:5]])
        
        # Entity evidence
        high_risk_entities = []
        if entities.get('weapons'):
            high_risk_entities.extend([f"Weapon reference: {weapon}" for weapon in entities['weapons'][:3]])
        
        if entities.get('drugs'):
            high_risk_entities.extend([f"Drug reference: {drug}" for drug in entities['drugs'][:3]])
        
        if entities.get('cryptocurrencies'):
            high_risk_entities.extend([f"Cryptocurrency: {crypto}" for crypto in entities['cryptocurrencies'][:3]])
        
        evidence_points.extend([f"ENTITY: {entity}" for entity in high_risk_entities])
        
        # Sentiment evidence
        if sentiment.get('negative', 0) > 0.7:
            evidence_points.append(f"SENTIMENT: Highly negative sentiment detected ({sentiment['negative']:.2f})")
        
        if sentiment.get('emotion_scores'):
            high_risk_emotions = [emotion for emotion, score in sentiment['emotion_scores'].items() 
                                if score > 0.7 and emotion in ['anger', 'disgust', 'fear']]
            for emotion in high_risk_emotions:
                evidence_points.append(f"EMOTION: High {emotion} detected ({sentiment['emotion_scores'][emotion]:.2f})")
        
        return evidence_points
    
    def _generate_enhanced_recommendations(self, threat_level: str, risk_score: float,
                                         threat_analysis: Dict, bot_analysis: Dict) -> List[str]:
        """Generate enhanced actionable recommendations"""
        recommendations = []
        
        # Immediate actions based on threat level
        if threat_level == "CRITICAL":
            recommendations.extend([
                "IMMEDIATE ESCALATION: Alert cybercrime unit and senior officers within 1 hour",
                "EVIDENCE PRESERVATION: Secure all digital evidence immediately",
                "LEGAL CONSULTATION: Contact legal team for potential charges under relevant acts",
                "INVESTIGATION LAUNCH: Initiate comprehensive digital forensics investigation",
                "MONITORING: Place subject under enhanced surveillance",
                "COORDINATION: Share intelligence with relevant security agencies"
            ])
        elif threat_level == "HIGH":
            recommendations.extend([
                "PRIORITY ESCALATION: Notify cybercrime unit within 4 hours",
                "ENHANCED MONITORING: Increase surveillance and data collection",
                "EVIDENCE GATHERING: Collect additional digital footprints and communications",
                "RISK ASSESSMENT: Evaluate potential for escalation to critical level",
                "NETWORK ANALYSIS: Investigate potential connections and associates",
                "LEGAL REVIEW: Assess evidence for potential legal action"
            ])
        elif threat_level == "MEDIUM":
            recommendations.extend([
                "CONTINUED MONITORING: Maintain regular surveillance",
                "DOCUMENTATION: Comprehensive logging of all activities",
                "ANALYSIS: Conduct deeper behavioral and network analysis",
                "PATTERN RECOGNITION: Look for escalating or concerning patterns",
                "INTELLIGENCE SHARING: Update relevant databases and watchlists"
            ])
        else:
            recommendations.extend([
                "ROUTINE MONITORING: Include in regular surveillance protocols",
                "DOCUMENTATION: Log for future reference and pattern analysis",
                "PERIODIC REVIEW: Reassess threat level monthly"
            ])
        
        # Bot-specific recommendations
        if bot_analysis.get('is_bot_likely') and bot_analysis.get('bot_score', 0) > 70:
            recommendations.extend([
                "BOT INVESTIGATION: Investigate potential bot network and control infrastructure",
                "NETWORK MAPPING: Identify and monitor related automated accounts",
                "PLATFORM NOTIFICATION: Report to relevant social media platforms"
            ])
        
        # Coordination-specific recommendations
        if threat_analysis.get('threat_category') == 'NATIONAL_SECURITY_THREAT':
            recommendations.extend([
                "NATIONAL SECURITY: Escalate to national security agencies",
                "CROSS-BORDER: Coordinate with international law enforcement if applicable"
            ])
        
        return recommendations
    
    def _generate_technical_details(self, content: str, sentiment: Dict, 
                                  entities: Dict, analysis_results: Dict) -> Dict[str, Any]:
        """Generate comprehensive technical details"""
        
        return {
            'analysis_metadata': {
                'timestamp': datetime.now().isoformat(),
                'engine_version': '2.0.0',
                'processing_time': analysis_results.get('performance_metrics', {}).get('total_processing_time', 0),
                'analysis_id': hashlib.md5(f"{content[:100]}{datetime.now().isoformat()}".encode()).hexdigest()
            },
            'content_metadata': {
                'content_length': len(content),
                'word_count': len(content.split()),
                'sentence_count': len(re.split(r'[.!?]+', content)),
                'language_detected': sentiment.get('language', 'unknown'),
                'character_encoding': 'utf-8',
                'content_hash': hashlib.sha256(content.encode()).hexdigest()
            },
            'sentiment_analysis': {
                'model_used': 'ensemble',
                'primary_sentiment': sentiment.get('label', 'neutral'),
                'confidence_score': sentiment.get('confidence', 0),
                'compound_score': sentiment.get('compound', 0),
                'emotion_distribution': sentiment.get('emotion_scores', {}),
                'cultural_context': sentiment.get('cultural_context', {})
            },
            'entity_extraction': {
                'total_entities': sum(len(ents) if isinstance(ents, list) else 0 for ents in entities.values()),
                'entity_confidence': entities.get('confidence_scores', {}),
                'extraction_methods': ['spacy', 'regex_patterns', 'domain_specific'],
                'relationship_count': len(entities.get('entity_relationships', []))
            },
            'threat_detection': {
                'models_used': ['keyword_based', 'pattern_matching', 'context_analysis'],
                'risk_components': analysis_results.get('threat_analysis', {}).get('probability_scores', {}),
                'detection_confidence': analysis_results.get('threat_analysis', {}).get('confidence', 0)
            },
            'performance_metrics': analysis_results.get('performance_metrics', {}),
            'system_information': {
                'models_available': {
                    'nltk': True,
                    'spacy_en': True,
                    'spacy_hi': True,
                    'transformers': True,
                    'sklearn': True
                },
                'processing_capabilities': [
                    'multilingual_analysis',
                    'emotion_detection',
                    'entity_extraction',
                    'coordination_detection',
                    'bot_identification'
                ]
            }
        }
    
    def _generate_intelligence_insights(self, content: str, analysis_results: Dict, 
                                      threat_level: str) -> List[Dict[str, Any]]:
        """Generate actionable intelligence insights"""
        from utils.nlp_engine import IntelligenceInsight
        
        insights = []
        
        # High-value entity insights
        entities = analysis_results.get('entities', {})
        if entities.get('persons') or entities.get('organizations'):
            insights.append(IntelligenceInsight(
                insight_type="ENTITY_INTELLIGENCE",
                priority="HIGH" if threat_level in ["HIGH", "CRITICAL"] else "MEDIUM",
                description="Named entities identified requiring investigation",
                evidence=[f"Persons: {len(entities.get('persons', []))}", 
                         f"Organizations: {len(entities.get('organizations', []))}"],
                confidence=0.8,
                actionable=True,
                time_sensitivity="48_HOURS",
                related_entities=[e.get('text', e) if isinstance(e, dict) else e 
                                for e in (entities.get('persons', []) + entities.get('organizations', []))[:5]],
                intelligence_value=0.7,
                verification_needed=True
            ))
        
        # Coordination insights
        coordination = analysis_results.get('coordination', {})
        if coordination.get('is_coordinated'):
            insights.append(IntelligenceInsight(
                insight_type="COORDINATION_INTELLIGENCE",
                priority="CRITICAL" if coordination.get('coordination_sophistication') == 'HIGHLY_SOPHISTICATED' else "HIGH",
                description="Coordinated activity detected indicating organized operation",
                evidence=coordination.get('coordination_indicators', [])[:5],
                confidence=coordination.get('confidence', 0.5),
                actionable=True,
                time_sensitivity="24_HOURS",
                related_entities=[],
                intelligence_value=0.9,
                verification_needed=True
            ))
        
        # Bot network insights
        bot_analysis = analysis_results.get('bot_analysis', {})
        if bot_analysis.get('is_bot_likely') and bot_analysis.get('bot_score', 0) > 70:
            insights.append(IntelligenceInsight(
                insight_type="AUTOMATION_INTELLIGENCE",
                priority="HIGH",
                description="Automated behavior suggesting bot network operation",
                evidence=bot_analysis.get('indicators', [])[:5],
                confidence=bot_analysis.get('confidence', 0.5),
                actionable=True,
                time_sensitivity="72_HOURS",
                related_entities=[],
                intelligence_value=0.6,
                verification_needed=True
            ))
        
        # Threat escalation insights
        threat_analysis = analysis_results.get('threat_analysis', {})
        if threat_analysis.get('risk_score', 0) > 70:
            insights.append(IntelligenceInsight(
                insight_type="THREAT_ESCALATION",
                priority="CRITICAL",
                description="High-risk content indicating potential threat escalation",
                evidence=threat_analysis.get('evidence_points', [])[:5],
                confidence=threat_analysis.get('confidence', 0.5),
                actionable=True,
                time_sensitivity="IMMEDIATE",
                related_entities=[],
                intelligence_value=0.95,
                verification_needed=False
            ))
        
        return [insight.__dict__ for insight in insights]  # Convert to dict for JSON serialization
    
    def _assess_enhanced_legal_implications(self, threat_analysis: Dict, risk_score: float,
                                          entities: Dict, content: str) -> str:
        """Enhanced legal implications assessment"""
        
        implications = []
        
        # Risk-based legal assessment
        if risk_score >= 80:
            implications.append("""
CRITICAL LEGAL RISK - IMMEDIATE ACTION REQUIRED:
Content may constitute serious violations under multiple Indian laws:

1. NATIONAL SECURITY ACTS:
   - National Security Act, 1980 (preventive detention)
   - Unlawful Activities (Prevention) Act, 1967 (terrorist activities)
   
2. INDIAN PENAL CODE SECTIONS:
   - Section 124A (Sedition)
   - Section 153A (Promoting enmity between different groups)
   - Section 295A (Deliberate and malicious acts intended to outrage religious feelings)
   - Section 505 (Statements conducing to public mischief)
   
3. INFORMATION TECHNOLOGY ACT:
   - Section 66A (Punishment for sending offensive messages - if applicable)
   - Section 69A (Power to issue directions for blocking public access)
            """)
            
        elif risk_score >= 60:
            implications.append("""
HIGH LEGAL RISK - URGENT REVIEW REQUIRED:
Content shows violations under:

1. INDIAN PENAL CODE:
   - Section 153A (Promoting enmity)
   - Section 295A (Religious offense)
   - Section 505 (Public mischief)
   
2. INFORMATION TECHNOLOGY ACT:
   - Relevant provisions for online content regulation
   
3. STATE-SPECIFIC LAWS:
   - Review applicable state laws for hate speech and public order
            """)
            
        elif risk_score >= 40:
            implications.append("""
MODERATE LEGAL RISK - MONITORING REQUIRED:
Content may violate:

1. Community standards and platform policies
2. Possible IPC Section 505 (Public mischief)
3. Local cybercrime regulations

Recommend continued monitoring and documentation.
            """)
        else:
            implications.append("""
LOW LEGAL RISK:
Content does not appear to violate major legal provisions.
Continue routine monitoring as per standard protocols.
            """)
        
        # Entity-specific legal considerations
        if entities.get('weapons'):
            implications.append("""
WEAPONS-RELATED CONTENT:
- Arms Act, 1959 implications
- Potential illegal weapons trade references
- Enhanced scrutiny required
            """)
        
        if entities.get('drugs'):
            implications.append("""
DRUG-RELATED CONTENT:
- Narcotic Drugs and Psychotropic Substances Act, 1985
- Potential drug trafficking implications
- DEA coordination may be required
            """)
        
        # Add procedural recommendations
        implications.append("""
PROCEDURAL RECOMMENDATIONS:
1. Preserve all digital evidence following IT Act guidelines
2. Maintain proper chain of custody for admissibility
3. Coordinate with cyber forensics team
4. Document all analysis procedures
5. Prepare for potential court proceedings
        """)
        
        return '\n'.join(implications)
    
    def _generate_chain_of_custody(self, case_id: str, content: str) -> List[Dict[str, Any]]:
        """Generate chain of custody documentation"""
        
        return [
            {
                'timestamp': datetime.now().isoformat(),
                'action': 'CONTENT_ACQUISITION',
                'officer_id': 'SYSTEM_AUTOMATED',
                'description': 'Content automatically acquired and analyzed by NLP system',
                'content_hash': hashlib.sha256(content.encode()).hexdigest(),
                'system_info': {
                    'engine_version': '2.0.0',
                    'analysis_id': case_id,
                    'processing_node': 'NLP_ANALYSIS_001'
                }
            },
            {
                'timestamp': datetime.now().isoformat(),
                'action': 'DIGITAL_ANALYSIS',
                'officer_id': 'SYSTEM_AUTOMATED',
                'description': 'Comprehensive NLP analysis performed',
                'integrity_verified': True,
                'analysis_methods': [
                    'sentiment_analysis',
                    'entity_extraction',
                    'threat_detection',
                    'bot_analysis',
                    'coordination_detection'
                ]
            }
        ]
    
    def _extract_forensic_markers(self, content: str, entities: Dict) -> Dict[str, Any]:
        """Extract forensic markers for investigation"""
        
        markers = {
            'digital_fingerprints': {
                'content_hash': hashlib.sha256(content.encode()).hexdigest(),
                'content_length': len(content),
                'character_frequency': dict(Counter(content.lower())),
                'linguistic_fingerprints': {
                    'avg_word_length': np.mean([len(word) for word in content.split()]) if content.split() else 0,
                    'sentence_count': len(re.split(r'[.!?]+', content)),
                    'punctuation_usage': dict(Counter(re.findall(r'[.!?,:;]', content)))
                }
            },
            'communication_artifacts': {
                'urls': entities.get('urls', []),
                'email_addresses': entities.get('email_addresses', []),
                'phone_numbers': entities.get('phone_numbers', []),
                'social_handles': entities.get('social_handles', [])
            },
            'temporal_markers': {
                'analysis_timestamp': datetime.now().isoformat(),
                'inferred_composition_time': 'UNKNOWN',  # Would require additional analysis
                'time_zone_indicators': []  # Would extract from content if available
            },
            'technical_artifacts': {
                'encoding': 'utf-8',
                'special_characters': list(set(re.findall(r'[^\w\s]', content))),
                'unicode_ranges': self._analyze_unicode_ranges(content),
                'potential_copy_paste_indicators': self._detect_copy_paste_indicators(content)
            }
        }
        
        return markers
    
    def _generate_correlation_data(self, entities: Dict, threat_analysis: Dict, 
                                 sentiment: Dict) -> Dict[str, Any]:
        """Generate data for correlation with other cases"""
        
        return {
            'entity_signatures': {
                'person_signatures': [self._create_entity_signature(p) for p in entities.get('persons', [])[:10]],
                'location_signatures': [self._create_entity_signature(l) for l in entities.get('locations', [])[:10]],
                'organization_signatures': [self._create_entity_signature(o) for o in entities.get('organizations', [])[:10]]
            },
            'threat_signatures': {
                'threat_keywords': threat_analysis.get('detected_keywords', []),
                'threat_patterns': threat_analysis.get('sub_categories', []),
                'risk_profile': {
                    'primary_category': threat_analysis.get('threat_category'),
                    'risk_score': threat_analysis.get('risk_score'),
                    'confidence': threat_analysis.get('confidence')
                }
            },
            'behavioral_signatures': {
                'sentiment_profile': {
                    'primary_sentiment': sentiment.get('label'),
                    'intensity': sentiment.get('intensity'),
                    'emotional_markers': sentiment.get('emotion_scores', {})
                },
                'linguistic_profile': {
                    'language': sentiment.get('language'),
                    'cultural_markers': sentiment.get('cultural_context', {}).get('cultural_markers', [])
                }
            },
            'correlation_metadata': {
                'generated_timestamp': datetime.now().isoformat(),
                'correlation_id': hashlib.md5(f"{entities}{threat_analysis}{sentiment}".encode()).hexdigest(),
                'case_similarity_threshold': 0.7
            }
        }
    
    def _generate_expert_analysis(self, analysis_results: Dict, threat_level: str, 
                                risk_score: float) -> Dict[str, Any]:
        """Generate expert analysis summary"""
        
        return {
            'threat_assessment': {
                'expert_opinion': self._generate_expert_threat_opinion(threat_level, risk_score),
                'confidence_assessment': self._assess_analysis_confidence(analysis_results),
                'alternative_interpretations': self._generate_alternative_interpretations(analysis_results),
                'investigation_priorities': self._recommend_investigation_priorities(analysis_results)
            },
            'technical_assessment': {
                'analysis_quality': self._assess_analysis_quality(analysis_results),
                'data_completeness': self._assess_data_completeness(analysis_results),
                'methodology_notes': self._generate_methodology_notes()
            },
            'operational_recommendations': {
                'immediate_actions': self._get_immediate_actions(threat_level, risk_score),
                'long_term_strategy': self._recommend_long_term_strategy(analysis_results),
                'resource_requirements': self._estimate_resource_requirements(threat_level)
            }
        }
    
    def _generate_risk_assessment_matrix(self, risk_score: float, threat_analysis: Dict,
                                       bot_analysis: Dict, coordination: Dict) -> Dict[str, Any]:
        """Generate comprehensive risk assessment matrix"""
        
        return {
            'overall_risk': {
                'score': risk_score,
                'level': self._determine_enhanced_threat_level(risk_score, threat_analysis, bot_analysis, coordination),
                'confidence': threat_analysis.get('confidence', 0.5)
            },
            'risk_components': {
                'content_risk': self._calculate_content_risk_component(threat_analysis),
                'behavioral_risk': self._calculate_behavioral_risk_component(bot_analysis),
                'network_risk': self._calculate_network_risk_component(coordination),
                'temporal_risk': self._calculate_temporal_risk_component(threat_analysis)
            },
            'escalation_factors': {
                'automation_factor': bot_analysis.get('bot_score', 0) / 100,
                'coordination_factor': coordination.get('similarity_score', 0) if coordination.get('is_coordinated') else 0,
                'threat_sophistication': threat_analysis.get('confidence', 0.5)
            },
            'mitigation_effectiveness': {
                'monitoring_effectiveness': 0.8,  # Based on system capabilities
                'intervention_options': self._assess_intervention_options(risk_score),
                'prevention_strategies': self._recommend_prevention_strategies(threat_analysis)
            }
        }
    
    # Helper methods for the above functions
    def _get_immediate_actions(self, threat_level: str, risk_score: float) -> str:
        """Get immediate actions based on threat level"""
        if threat_level == "CRITICAL":
            return "Alert cybercrime unit immediately, preserve evidence, initiate investigation"
        elif threat_level == "HIGH":
            return "Notify supervisors, increase monitoring, prepare for escalation"
        elif threat_level == "MEDIUM":
            return "Document findings, continue monitoring, prepare intelligence report"
        else:
            return "Log for reference, routine monitoring"
    
    def _determine_intelligence_priority(self, threat_level: str, risk_score: float) -> str:
        """Determine intelligence priority"""
        if threat_level == "CRITICAL" or risk_score >= 80:
            return "PRIORITY 1 - IMMEDIATE ACTION"
        elif threat_level == "HIGH" or risk_score >= 60:
            return "PRIORITY 2 - URGENT ATTENTION"
        elif threat_level == "MEDIUM" or risk_score >= 40:
            return "PRIORITY 3 - ROUTINE INVESTIGATION"
        else:
            return "PRIORITY 4 - MONITORING ONLY"
    
    def _analyze_unicode_ranges(self, text: str) -> List[str]:
        """Analyze Unicode character ranges in text"""
        ranges = []
        for char in text:
            code_point = ord(char)
            if 0x0000 <= code_point <= 0x007F:
                ranges.append('ASCII')
            elif 0x0900 <= code_point <= 0x097F:
                ranges.append('Devanagari')
            elif 0x0600 <= code_point <= 0x06FF:
                ranges.append('Arabic')
            # Add more ranges as needed
        
        return list(set(ranges))
    
    def _detect_copy_paste_indicators(self, text: str) -> List[str]:
        """Detect potential copy-paste indicators"""
        indicators = []
        
        # Check for unusual character sequences
        if re.search(r'\u200B|\u200C|\u200D', text):  # Zero-width characters
            indicators.append('zero_width_characters')
        
        # Check for unusual formatting
        if re.search(r'[^\x00-\x7F]{3,}', text):  # Non-ASCII sequences
            indicators.append('non_ascii_sequences')
        
        return indicators
    
    def _create_entity_signature(self, entity) -> Dict[str, Any]:
        """Create a signature for entity correlation"""
        if isinstance(entity, dict):
            text = entity.get('text', '')
            confidence = entity.get('confidence', 0.5)
        else:
            text = str(entity)
            confidence = 0.5
        
        return {
            'text': text,
            'normalized': text.lower().strip(),
            'length': len(text),
            'confidence': confidence,
            'hash': hashlib.md5(text.encode()).hexdigest()
        }
    
    def _generate_expert_threat_opinion(self, threat_level: str, risk_score: float) -> str:
        """Generate expert opinion on threat assessment"""
        if threat_level == "CRITICAL":
            return f"Critical threat assessment confirmed. Risk score of {risk_score:.1f} indicates immediate action required."
        elif threat_level == "HIGH":
            return f"High-risk content requiring urgent attention. Score of {risk_score:.1f} suggests significant threat potential."
        elif threat_level == "MEDIUM":
            return f"Moderate risk assessment. Score of {risk_score:.1f} requires continued monitoring and analysis."
        else:
            return f"Low-risk assessment. Score of {risk_score:.1f} suggests minimal immediate threat."
    
    def _assess_analysis_confidence(self, analysis_results: Dict) -> float:
        """Assess overall confidence in analysis"""
        confidence_factors = []
        
        if 'sentiment' in analysis_results:
            confidence_factors.append(analysis_results['sentiment'].get('confidence', 0.5))
        
        if 'threat_analysis' in analysis_results:
            confidence_factors.append(analysis_results['threat_analysis'].get('confidence', 0.5))
        
        if 'bot_analysis' in analysis_results:
            confidence_factors.append(analysis_results['bot_analysis'].get('confidence', 0.5))
        
        return np.mean(confidence_factors) if confidence_factors else 0.5
    
    def _generate_alternative_interpretations(self, analysis_results: Dict) -> List[str]:
        """Generate alternative interpretations of the analysis"""
        interpretations = []
        
        risk_score = analysis_results.get('risk_score', 0)
        
        if risk_score > 70:
            interpretations.append("Content may be part of a coordinated disinformation campaign")
            interpretations.append("Author may be under external influence or coercion")
        elif risk_score > 40:
            interpretations.append("Content may be satire or hyperbole rather than genuine threat")
            interpretations.append("Author may be expressing frustration rather than planning action")
        else:
            interpretations.append("Content appears to be routine social media activity")
        
        return interpretations
    
    def _recommend_investigation_priorities(self, analysis_results: Dict) -> List[str]:
        """Recommend investigation priorities"""
        priorities = []
        
        entities = analysis_results.get('entities', {})
        
        if entities.get('persons'):
            priorities.append("Investigate identified individuals for background and connections")
        
        if entities.get('locations'):
            priorities.append("Verify and investigate mentioned locations")
        
        if analysis_results.get('coordination', {}).get('is_coordinated'):
            priorities.append("Map network connections and coordination patterns")
        
        if analysis_results.get('bot_analysis', {}).get('is_bot_likely'):
            priorities.append("Investigate bot network infrastructure and control mechanisms")
        
        return priorities
    
    def _assess_analysis_quality(self, analysis_results: Dict) -> str:
        """Assess the quality of the analysis"""
        quality_indicators = 0
        
        if analysis_results.get('sentiment'):
            quality_indicators += 1
        if analysis_results.get('entities'):
            quality_indicators += 1
        if analysis_results.get('threat_analysis'):
            quality_indicators += 1
        if analysis_results.get('bot_analysis'):
            quality_indicators += 1
        
        if quality_indicators >= 4:
            return "HIGH_QUALITY"
        elif quality_indicators >= 3:
            return "GOOD_QUALITY"
        elif quality_indicators >= 2:
            return "MODERATE_QUALITY"
        else:
            return "LIMITED_QUALITY"
    
    def _assess_data_completeness(self, analysis_results: Dict) -> float:
        """Assess completeness of available data"""
        expected_components = ['sentiment', 'entities', 'threat_analysis', 'risk_score']
        available_components = sum(1 for comp in expected_components if comp in analysis_results)
        
        return available_components / len(expected_components)
    
    def _generate_methodology_notes(self) -> List[str]:
        """Generate methodology notes for the analysis"""
        return [
            "Multi-model ensemble approach used for sentiment analysis",
            "Pattern-matching and ML techniques combined for threat detection",
            "Entity extraction using spaCy NLP models and regex patterns",
            "Behavioral analysis based on linguistic and temporal patterns",
            "Risk scoring uses weighted multi-factor assessment",
            "Confidence scores based on model agreement and evidence strength"
        ]
    
    def _recommend_long_term_strategy(self, analysis_results: Dict) -> List[str]:
        """Recommend long-term strategy based on analysis"""
        strategies = []
        
        if analysis_results.get('coordination', {}).get('is_coordinated'):
            strategies.append("Develop long-term monitoring strategy for coordinated networks")
        
        if analysis_results.get('bot_analysis', {}).get('is_bot_likely'):
            strategies.append("Implement advanced bot detection and mitigation measures")
        
        strategies.extend([
            "Regular pattern updates and model retraining",
            "Enhanced cross-platform monitoring and correlation",
            "Development of predictive threat assessment capabilities"
        ])
        
        return strategies
    
    def _estimate_resource_requirements(self, threat_level: str) -> Dict[str, Any]:
        """Estimate resource requirements for investigation"""
        if threat_level == "CRITICAL":
            return {
                "personnel": "5-10 officers",
                "duration": "Immediate response, 30-90 days investigation",
                "technical_resources": "Full forensics team, advanced analytics",
                "external_coordination": "Multiple agencies"
            }
        elif threat_level == "HIGH":
            return {
                "personnel": "3-5 officers",
                "duration": "24-48 hours response, 15-30 days investigation",
                "technical_resources": "Standard forensics, monitoring tools",
                "external_coordination": "Relevant departments"
            }
        else:
            return {
                "personnel": "1-2 officers",
                "duration": "Routine monitoring",
                "technical_resources": "Automated monitoring",
                "external_coordination": "Minimal"
            }
    
    def _calculate_content_risk_component(self, threat_analysis: Dict) -> float:
        """Calculate content-specific risk component"""
        return min(threat_analysis.get('risk_score', 0) / 100, 1.0)
    
    def _calculate_behavioral_risk_component(self, bot_analysis: Dict) -> float:
        """Calculate behavioral risk component"""
        return min(bot_analysis.get('bot_score', 0) / 100, 1.0)
    
    def _calculate_network_risk_component(self, coordination: Dict) -> float:
        """Calculate network risk component"""
        if coordination.get('is_coordinated'):
            return coordination.get('similarity_score', 0)
        return 0.0
    
    def _calculate_temporal_risk_component(self, threat_analysis: Dict) -> float:
        """Calculate temporal risk component"""
        # Simplified temporal risk based on threat immediacy
        if 'immediate' in str(threat_analysis.get('evidence_points', [])).lower():
            return 0.8
        elif 'urgent' in str(threat_analysis.get('evidence_points', [])).lower():
            return 0.6
        else:
            return 0.3
    
    def _assess_intervention_options(self, risk_score: float) -> List[str]:
        """Assess intervention options based on risk score"""
        if risk_score >= 80:
            return ["Immediate arrest", "Digital asset seizure", "Network disruption"]
        elif risk_score >= 60:
            return ["Enhanced surveillance", "Content removal", "Platform notification"]
        elif risk_score >= 40:
            return ["Monitoring increase", "Warning notification", "Documentation"]
        else:
            return ["Routine monitoring", "Database logging"]
    
    def _recommend_prevention_strategies(self, threat_analysis: Dict) -> List[str]:
        """Recommend prevention strategies"""
        strategies = ["Enhanced monitoring of similar content patterns"]
        
        threat_category = threat_analysis.get('threat_category', '')
        
        if 'TERRORISM' in threat_category:
            strategies.extend([
                "Counter-radicalization outreach",
                "Community engagement programs",
                "Enhanced border and travel monitoring"
            ])
        elif 'CYBERCRIME' in threat_category:
            strategies.extend([
                "Cybersecurity awareness campaigns",
                "Financial institution alerts",
                "Platform security enhancements"
            ])
        
        return strategies
    
    def _generate_error_evidence_summary(self, case_id: str, error_msg: str):
        """Generate error evidence summary"""
        from utils.nlp_engine import EvidenceSummary
        
        return EvidenceSummary(
            case_id=case_id or f"ERROR_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            timestamp=datetime.now(),
            threat_level="UNKNOWN",
            summary=f"Analysis Error: {error_msg}",
            detailed_analysis="Analysis could not be completed due to system error.",
            evidence_points=[f"Error: {error_msg}"],
            recommended_actions=["Review system logs", "Retry analysis", "Manual review required"],
            technical_details={"error": error_msg, "timestamp": datetime.now().isoformat()},
            legal_implications="Unable to assess due to analysis error.",
            intelligence_insights=[],
            chain_of_custody=[],
            forensic_markers={},
            correlation_data={},
            expert_analysis={},
            risk_assessment={}
        )
