# Signatures Numériques

## Bon à savoir

Le projet comporte une version de code python en mode présenté (fichiers jupyter notebooks (.ipynb)) formée des codes suivants:

- `Signature.ipynb`: ce fichier contient le code qui permet à l'envoyeur de signer son message.
- `Vérification.ipynb`: ce fichier contient le code qui permet au destinataire de vérifier l'intégrité du message.

Le projet dispose également d'une version de programmes python natifs ('.py') qui sont des réécritures des fichiers ci-dessus sous forme de programme tout court.

## Comment fonctionne le projet

1. L'envoyeur copie son message dans le fichier `message.txt` qui se trouve dans le dossier `Signature`.
2. Ensuite, il exécute le programme `Signature.py`, qui utilise la clé privée stockée dans le fichier `PrivateKey.txt`, pour signer son message.
3. La clé privée est automatiquement générée et stockée dans le fichier `PrivateKey.txt`.
4. Une fois que le message est signé, la clé publique correspondante est stockée dans le fichier `PublicKey.txt` et le message signé est stocké dans le fichier `SignedMessage.txt`, tous deux situés dans le dossier `Signature`.
5. Pour transmettre le message signé au destinataire, il suffit d'envoyer le dossier `Signature` qui contient également le message en clair.
6. Le destinataire reçoit le dossier `Signature` et exécute le fichier `Vérification.py`. Ce programme utilise la clé publique du fichier `PublicKey.txt` et le message signé du fichier `SignedMessage.txt` pour vérifier l'intégrité du message.
   - Si le message est intègre, le programme affiche un message indiquant que le message est valide.
   - Si le message a été modifié, le programme affiche un message indiquant que le message est invalide.

## A propos

Ce projet a été réalisé par des étudiants du 3GI ENSPY Promotion 2026:

- KAMDEM POUOKAM IVANN HAROLD
- KENFACK NOUMEDEM FRANCK ULRICH
- WADOH TCHINDA PAVEL DIOR
- KENGNE TUEGUEM FRESNEL GRÂCE
- BIHAY RAPHAEL
