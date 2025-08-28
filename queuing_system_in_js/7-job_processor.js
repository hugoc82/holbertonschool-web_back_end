// 7-job_processor.js
import kue from 'kue';

const queue = kue.createQueue();

// Liste noire de numéros de téléphone
const blacklistedNumbers = ['4153518780', '4153518781'];

/**
 * Fonction pour envoyer une notification
 */
function sendNotification(phoneNumber, message, job, done) {
  // Début du traitement → 0% progress
  job.progress(0, 100);

  // Vérifier si le numéro est blacklisté
  if (blacklistedNumbers.includes(phoneNumber)) {
    return done(new Error(`Phone number ${phoneNumber} is blacklisted`));
  }

  // Avancement 50%
  job.progress(50, 100);

  console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);

  // Fin avec succès
  done();
}

// On configure la queue pour traiter 2 jobs en parallèle
queue.process('push_notification_code_2', 2, (job, done) => {
  const { phoneNumber, message } = job.data;
  sendNotification(phoneNumber, message, job, done);
});

