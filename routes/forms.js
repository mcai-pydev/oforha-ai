const express = require('express');
const router = express.Router();
const Form = require('../models/form');

// Create new form
router.post('/', async (req, res) => {
  try {
    const form = new Form(req.body);
    await form.save();
    res.status(201).json(form);
  } catch (error) {
    res.status(500).json({ message: 'Error creating form', error: error.message });
  }
});

// Submit form data
router.post('/:formId/submit', async (req, res) => {
  try {
    const form = await Form.findById(req.params.formId);
    if (!form) {
      return res.status(404).json({ message: 'Form not found' });
    }

    const submission = {
      data: req.body,
      submittedBy: req.user?.userId // If user is logged in
    };

    form.submissions.push(submission);
    await form.save();

    // Handle form settings (notifications, auto-reply, etc.)
    if (form.settings.notifications.email) {
      // Send email notification
    }

    if (form.settings.autoReply) {
      // Send auto-reply email
    }

    res.status(201).json({ message: 'Form submitted successfully' });
  } catch (error) {
    res.status(500).json({ message: 'Error submitting form', error: error.message });
  }
});

// Get form submissions (admin only)
router.get('/:formId/submissions', async (req, res) => {
  try {
    const form = await Form.findById(req.params.formId)
      .populate('submissions.submittedBy', 'email name');
    
    if (!form) {
      return res.status(404).json({ message: 'Form not found' });
    }

    res.json(form.submissions);
  } catch (error) {
    res.status(500).json({ message: 'Error fetching submissions', error: error.message });
  }
});

// Update submission status
router.patch('/:formId/submissions/:submissionId', async (req, res) => {
  try {
    const form = await Form.findById(req.params.formId);
    if (!form) {
      return res.status(404).json({ message: 'Form not found' });
    }

    const submission = form.submissions.id(req.params.submissionId);
    if (!submission) {
      return res.status(404).json({ message: 'Submission not found' });
    }

    submission.status = req.body.status;
    await form.save();

    res.json(submission);
  } catch (error) {
    res.status(500).json({ message: 'Error updating submission', error: error.message });
  }
});

module.exports = router; 