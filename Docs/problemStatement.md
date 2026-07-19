# AI-Powered Discovery Engine — Problem Statement (Swiggy Instamart)
*Note: This document is scoped specifically to Part 1 of the Growth Team project.*

## Introduction
Quick commerce platforms have successfully become a part of users' weekly routines. Many users place recurring orders for Groceries, snacks & beverages, and household essentials. However, over time, shopping behavior becomes highly repetitive. Users often purchase the same set of products repeatedly and rarely explore new categories available on the platform.

We are building an **AI-powered Discovery Engine** to analyze unstructured user feedback at scale. This system aims to uncover the root causes behind "Category Inertia" on Swiggy Instamart.

## Strategic Goal
Increase the percentage of Monthly Active Customers (MAC) who purchase products from at least one new category every month.
*Examples:*
- A user who buys groceries starts buying pet supplies.
- A user who buys snacks starts buying personal care products.

## Part 1: The Discovery Engine Scope

### 1. Ingestion Sources
The system will aggregate and analyze unstructured feedback exclusively for the **Swiggy Instamart platform** from the following sources:
- App Store reviews
- Play Store reviews
- Reddit discussions
- Community forums
- Social media conversations
- Product reviews
- Quick-commerce discussions

### 2. Core Strategic Questions
The AI reasoning engine is designed to explicitly answer the following research questions based on the aggregated data:
1. Why do users repeatedly buy from the same categories?
2. What prevents users from exploring new categories?
3. How do users discover products today?
4. What role do habits play in shopping behavior?
5. What information do users need before trying a new category?
6. What frustrations emerge repeatedly?
7. Which user segments are more likely to experiment?
8. What unmet needs emerge consistently across discussions?

### 3. Deliverables & Demonstration Requirements
The Discovery Engine workflow must clearly demonstrate:
- **Data Gathering**: How the scripts and APIs pull data from the sources.
- **Theme Identification**: How the text is processed and clustered into themes.
- **Insight Generation**: How the LLM synthesizes the themes to answer the core strategic questions.
- **Quality Validation**: Traceability ensuring that generated insights can be linked back to real user quotes (auditability) before moving on to primary user research.
