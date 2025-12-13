#!/usr/bin/env python3
"""
Conversation Analyzer - Extracts improvement opportunities from conversation history

This script analyzes conversation context to identify:
- Skills and plugins that were used or mentioned
- User feedback (positive and negative)
- Issues, errors, or pain points
- Feature requests and enhancement suggestions
- Gaps between expected and actual skill/plugin behavior

Usage:
    python analyze_conversation.py

The script expects conversation data to be piped in or provided via stdin.
"""

import json
import re
import sys
from typing import Dict, List, Set
from dataclasses import dataclass, asdict


@dataclass
class ConversationInsight:
    """Represents an insight extracted from conversation"""
    type: str  # 'feedback', 'error', 'feature_request', 'usage_pattern'
    skill_or_plugin: str  # Name of the skill/plugin
    description: str  # What was observed
    severity: str  # 'high', 'medium', 'low'
    quote: str  # Relevant quote from conversation


@dataclass
class ImprovementSuggestion:
    """Represents a suggested improvement"""
    target: str  # Skill/plugin name
    category: str  # 'description', 'content', 'script', 'metadata'
    suggestion: str  # What to improve
    rationale: str  # Why this improvement is needed
    priority: str  # 'high', 'medium', 'low'


class ConversationAnalyzer:
    """Analyzes conversation history for improvement opportunities"""

    def __init__(self):
        self.insights: List[ConversationInsight] = []
        self.suggestions: List[ImprovementSuggestion] = []

    def analyze(self, conversation_text: str) -> Dict:
        """
        Main analysis method.

        Args:
            conversation_text: Full conversation history

        Returns:
            Dictionary containing insights and suggestions
        """
        # Extract skills/plugins mentioned
        skills_mentioned = self._extract_skills_plugins(conversation_text)

        # Identify feedback patterns
        feedback_insights = self._extract_feedback(conversation_text, skills_mentioned)
        self.insights.extend(feedback_insights)

        # Identify errors and issues
        error_insights = self._extract_errors(conversation_text, skills_mentioned)
        self.insights.extend(error_insights)

        # Identify feature requests
        feature_insights = self._extract_feature_requests(conversation_text, skills_mentioned)
        self.insights.extend(feature_insights)

        # Generate improvement suggestions
        self.suggestions = self._generate_suggestions()

        return {
            'skills_mentioned': list(skills_mentioned),
            'insights': [asdict(i) for i in self.insights],
            'suggestions': [asdict(s) for s in self.suggestions]
        }

    def _extract_skills_plugins(self, text: str) -> Set[str]:
        """Extract skill and plugin names mentioned in conversation"""
        skills = set()

        # Look for skill invocations
        skill_patterns = [
            r'skill[:\s]+([a-z-]+)',
            r'using (?:the )?([a-z-]+) skill',
            r'invoke[d]? (?:the )?([a-z-]+) skill',
            r'([a-z-]+)\.skill',
        ]

        for pattern in skill_patterns:
            matches = re.finditer(pattern, text.lower())
            for match in matches:
                skills.add(match.group(1))

        # Look for plugin mentions
        plugin_patterns = [
            r'plugin[:\s]+([a-z-]+)',
            r'([a-z-]+) plugin',
            r'plugin\.json.*name.*?["\']([a-z-]+)["\']',
        ]

        for pattern in plugin_patterns:
            matches = re.finditer(pattern, text.lower())
            for match in matches:
                skills.add(match.group(1))

        return skills

    def _extract_feedback(self, text: str, targets: Set[str]) -> List[ConversationInsight]:
        """Extract explicit feedback about skills/plugins"""
        insights = []

        # Positive feedback patterns
        positive_patterns = [
            r'(works? well|great|perfect|excellent|helpful)',
            r'(successfully|correctly) (processed|handled|created)',
        ]

        # Negative feedback patterns
        negative_patterns = [
            r"(doesn't work|failed|broken|not working)",
            r'(confused|unclear|missing|lacking)',
            r'(should have|wish it had|would be better if)',
        ]

        # Look for feedback in context of each target
        for target in targets:
            context_pattern = rf'.{{0,100}}{target}.{{0,100}}'
            contexts = re.finditer(context_pattern, text.lower(), re.DOTALL)

            for context_match in contexts:
                context = context_match.group(0)

                # Check for negative feedback
                for pattern in negative_patterns:
                    if re.search(pattern, context):
                        insights.append(ConversationInsight(
                            type='feedback',
                            skill_or_plugin=target,
                            description='Negative feedback detected',
                            severity='high',
                            quote=context[:200]
                        ))
                        break

        return insights

    def _extract_errors(self, text: str, targets: Set[str]) -> List[ConversationInsight]:
        """Extract error messages and issues"""
        insights = []

        # Error patterns
        error_patterns = [
            r'error:?\s+(.+)',
            r'exception:?\s+(.+)',
            r'failed to (.+)',
            r'could not (.+)',
            r'❌ (.+)',
        ]

        for pattern in error_patterns:
            matches = re.finditer(pattern, text.lower())
            for match in matches:
                error_desc = match.group(1)[:200]

                # Try to associate with a skill/plugin
                associated_target = None
                for target in targets:
                    if target in match.group(0).lower():
                        associated_target = target
                        break

                if associated_target:
                    insights.append(ConversationInsight(
                        type='error',
                        skill_or_plugin=associated_target,
                        description=f'Error encountered: {error_desc}',
                        severity='high',
                        quote=match.group(0)[:200]
                    ))

        return insights

    def _extract_feature_requests(self, text: str, targets: Set[str]) -> List[ConversationInsight]:
        """Extract feature requests and enhancement ideas"""
        insights = []

        # Feature request patterns
        request_patterns = [
            r'(should|could|would like to|want to|need to) (.+)',
            r'(add|include|support) (.+)',
            r'(missing|lacking|doesn\'t have) (.+)',
        ]

        for target in targets:
            context_pattern = rf'.{{0,150}}{target}.{{0,150}}'
            contexts = re.finditer(context_pattern, text.lower(), re.DOTALL)

            for context_match in contexts:
                context = context_match.group(0)

                for pattern in request_patterns:
                    match = re.search(pattern, context)
                    if match:
                        insights.append(ConversationInsight(
                            type='feature_request',
                            skill_or_plugin=target,
                            description=f'Feature request: {match.group(2)[:100]}',
                            severity='medium',
                            quote=context[:200]
                        ))
                        break

        return insights

    def _generate_suggestions(self) -> List[ImprovementSuggestion]:
        """Generate improvement suggestions based on insights"""
        suggestions = []

        # Group insights by target
        by_target = {}
        for insight in self.insights:
            target = insight.skill_or_plugin
            if target not in by_target:
                by_target[target] = []
            by_target[target].append(insight)

        # Generate suggestions for each target
        for target, target_insights in by_target.items():
            # Check for description improvements needed
            feedback_count = sum(1 for i in target_insights if i.type == 'feedback')
            if feedback_count > 0:
                suggestions.append(ImprovementSuggestion(
                    target=target,
                    category='description',
                    suggestion='Update skill/plugin description to better match actual usage',
                    rationale=f'Found {feedback_count} feedback items indicating description mismatch',
                    priority='high'
                ))

            # Check for content improvements
            error_count = sum(1 for i in target_insights if i.type == 'error')
            if error_count > 0:
                suggestions.append(ImprovementSuggestion(
                    target=target,
                    category='content',
                    suggestion='Add error handling guidance and troubleshooting steps',
                    rationale=f'Found {error_count} errors that could be addressed in documentation',
                    priority='high'
                ))

            # Check for feature additions
            feature_count = sum(1 for i in target_insights if i.type == 'feature_request')
            if feature_count > 0:
                suggestions.append(ImprovementSuggestion(
                    target=target,
                    category='content',
                    suggestion='Add requested features or document limitations',
                    rationale=f'Found {feature_count} feature requests from users',
                    priority='medium'
                ))

        return suggestions


def main():
    """Main entry point"""
    # Read conversation from stdin
    if sys.stdin.isatty():
        print("Usage: python analyze_conversation.py < conversation.txt")
        print("   or: echo 'conversation text' | python analyze_conversation.py")
        sys.exit(1)

    conversation_text = sys.stdin.read()

    # Analyze conversation
    analyzer = ConversationAnalyzer()
    results = analyzer.analyze(conversation_text)

    # Output results as JSON
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
