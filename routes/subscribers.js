const express = require('express');
const router = express.Router();
const Subscriber = require('../models/subscriber');

// Subscribe to newsletter
router.post('/subscribe', async (req, res) => {
  try {
    const { email, name, preferences } = req.body;

    // Check if already subscribed
    const existingSubscriber = await Subscriber.findOne({ email });
    if (existingSubscriber) {
      if (existingSubscriber.status === 'unsubscribed') {
        // Reactivate subscriber
        existingSubscriber.status = 'active';
        existingSubscriber.unsubscribeDate = null;
        await existingSubscriber.save();
        return res.json({ message: 'Successfully resubscribed' });
      }
      return res.status(400).json({ message: 'Already subscribed' });
    }

    // Create new subscriber
    const subscriber = new Subscriber({
      email,
      name,
      preferences,
      metadata: {
        source: req.body.source,
        ipAddress: req.ip,
        userAgent: req.get('user-agent')
      }
    });

    await subscriber.save();

    // Send welcome email
    // TODO: Implement email sending

    res.status(201).json({ message: 'Successfully subscribed' });
  } catch (error) {
    res.status(500).json({ message: 'Error subscribing', error: error.message });
  }
});

// Unsubscribe from newsletter
router.post('/unsubscribe', async (req, res) => {
  try {
    const { email } = req.body;

    const subscriber = await Subscriber.findOne({ email });
    if (!subscriber) {
      return res.status(404).json({ message: 'Subscriber not found' });
    }

    subscriber.status = 'unsubscribed';
    subscriber.unsubscribeDate = new Date();
    await subscriber.save();

    res.json({ message: 'Successfully unsubscribed' });
  } catch (error) {
    res.status(500).json({ message: 'Error unsubscribing', error: error.message });
  }
});

// Update subscriber preferences
router.patch('/preferences', async (req, res) => {
  try {
    const { email, preferences } = req.body;

    const subscriber = await Subscriber.findOne({ email });
    if (!subscriber) {
      return res.status(404).json({ message: 'Subscriber not found' });
    }

    subscriber.preferences = preferences;
    await subscriber.save();

    res.json({ message: 'Preferences updated successfully' });
  } catch (error) {
    res.status(500).json({ message: 'Error updating preferences', error: error.message });
  }
});

// Get subscriber stats (admin only)
router.get('/stats', async (req, res) => {
  try {
    const stats = await Subscriber.aggregate([
      {
        $group: {
          _id: '$status',
          count: { $sum: 1 }
        }
      }
    ]);

    const totalSubscribers = await Subscriber.countDocuments();
    const recentSubscribers = await Subscriber.find()
      .sort({ subscribedAt: -1 })
      .limit(10);

    res.json({
      stats,
      totalSubscribers,
      recentSubscribers
    });
  } catch (error) {
    res.status(500).json({ message: 'Error fetching stats', error: error.message });
  }
});

module.exports = router; 