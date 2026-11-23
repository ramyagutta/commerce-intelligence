# Ticket Taxonomy & Intelligence Requirements

**Project:** AI Commerce Intelligence  
**Version:** 0.1

## 1. Purpose

Define a structured taxonomy for understanding e-commerce customer support tickets. This taxonomy will be used for synthetic ticket generation, model training, evaluation, routing and downstream analytics.

## 2. Primary Issue Categories

- Delivery
- Product
- Refund & Return
- Payment
- Cancellation
- Seller
- Account
- Other

## 3. Issue Types

### Delivery
- Delayed shipment
- Tracking issue
- Order not received
- Failed delivery
- Address issue

### Product
- Damaged product
- Defective product
- Wrong product
- Missing item
- Quality complaint

### Refund & Return
- Refund request
- Refund delayed
- Return request
- Return status inquiry
- Refund dispute

### Payment
- Payment failure
- Duplicate charge
- Payment pending
- Payment discrepancy

### Cancellation
- Cancellation request
- Cancellation failure
- Cancellation confirmation inquiry

Additional issue types for Seller, Account and Other will be defined during data design.

## 4. Customer Intent

Initial intent labels:

- Information Request
- Status Inquiry
- Refund Request
- Return Request
- Cancellation Request
- Replacement Request
- Complaint
- Resolution Follow-up
- Other

Intent may be multi-label.

## 5. Sentiment

- Positive
- Neutral
- Negative

Sentiment must be evaluated independently of urgency.

## 6. Urgency

- Low
- Medium
- High
- Critical

Urgency may depend on message content, issue type, order context, previous interactions and business rules.

## 7. Confidence

The system must produce prediction confidence and support configurable confidence-based routing.

Confidence thresholds must be determined empirically using validation data and calibration.

## 8. Uncertainty Handling

The system must support:

- Low-confidence predictions.
- Ambiguous tickets.
- Missing information.
- Human escalation.
- Clarification requests.
- Abstention where reliable predictions cannot be made.

## 9. Initial Prediction Tasks

- Issue category classification.
- Issue type classification.
- Customer intent prediction.
- Sentiment classification.
- Urgency prediction.
- Confidence estimation.

## 10. Design Considerations

- Category and intent must remain separate.
- A ticket may contain multiple intents.
- Sentiment and urgency must not be treated as equivalent.
- Unknown issues must not be forced into an incorrect class.
- The taxonomy may evolve based on dataset analysis.
- Changes to the taxonomy must be versioned and documented.
- Evaluation must account for class imbalance.
- Synthetic data must maintain consistent ground truth.

## 11. Future Evaluation

Classification models will be evaluated using suitable metrics including:

- Accuracy
- Precision
- Recall
- Macro-F1
- Weighted-F1
- Confusion matrix
- Confidence calibration

Metric selection will depend on the task and its business impact.
