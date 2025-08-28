// 8-job.test.js
import kue from 'kue';
import { expect } from 'chai';
import createPushNotificationsJobs from './8-job.js';

describe('createPushNotificationsJobs', () => {
  let queue;

  beforeEach(() => {
    queue = kue.createQueue();
    // Entrer en mode test AVANT d'ajouter des jobs
    queue.testMode.enter();
  });

  afterEach(() => {
    // Nettoyer et quitter le mode test APRÈS chaque test
    queue.testMode.clear();
    queue.testMode.exit();
  });

  it('display a error message if jobs is not an array', () => {
    expect(() => createPushNotificationsJobs({}, queue)).to.throw('Jobs is not an array');
    expect(() => createPushNotificationsJobs('not an array', queue)).to.throw('Jobs is not an array');
    expect(() => createPushNotificationsJobs(null, queue)).to.throw('Jobs is not an array');
  });

  it('create two new jobs to the queue', () => {
    const jobs = [
      { phoneNumber: '4153518780', message: 'This is the code 1234 to verify your account' },
      { phoneNumber: '4153518781', message: 'This is the code 4562 to verify your account' },
    ];

    createPushNotificationsJobs(jobs, queue);

    // Vérifie le nombre de jobs créés
    expect(queue.testMode.jobs.length).to.equal(2);

    // Vérifie type + data du premier job
    expect(queue.testMode.jobs[0].type).to.equal('push_notification_code_3');
    expect(queue.testMode.jobs[0].data).to.deep.equal(jobs[0]);

    // Vérifie type + data du deuxième job
    expect(queue.testMode.jobs[1].type).to.equal('push_notification_code_3');
    expect(queue.testMode.jobs[1].data).to.deep.equal(jobs[1]);
  });
});

