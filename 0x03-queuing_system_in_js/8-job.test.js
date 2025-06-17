import { expect } from 'chai';
import kue from 'kue';
import createPushNotificationsJobs from './8-job.js';

const queue = kue.createQueue();

describe('createPushNotificationsJobs', () => {
  before(() => {
    queue.testMode.enter();
  });

  after(() => {
    queue.testMode.clear();
    queue.testMode.exit();
  });

  it('should throw an error if jobs is not an array', () => {
    expect(() => createPushNotificationsJobs('not an array', queue))
      .to.throw('Jobs is not an array');
  });

  it('should create two new jobs to the queue', () => {
    const jobs = [
      {
        phoneNumber: '415318781',
        message: 'This is a phone number',
      },
      {
        phoneNumber: '415318782',
        message: 'This is also a phone number',
      },
    ];

    createPushNotificationsJobs(jobs, queue);
    expect(queue.testMode.jobs.length).to.equal(2);

    expect(queue.testMode.jobs[0].data).to.deep.equal(jobs[0]);
    expect(queue.testMode.jobs[0].type).to.equal('push_notification_code_3');

    expect(queue.testMode.jobs[1].data).to.deep.equal(jobs[1]);
    expect(queue.testMode.jobs[1].type).to.equal('push_notification_code_3');
  });
});
