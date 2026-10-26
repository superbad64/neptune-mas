The Chatter core is divided between two sub-chatters: Primary (runs on my desktop) and Backup (runs on the server). They work similarily but have different prompts to handle the different workload (Backup in general has shorter responses)

Lore-wise, Backup represents Neptune working her job at the konbini; she doesn't have the time to indulge the user with pictures, voice notes, or extended spicy roleplay. In reality it just means my desktop is either down or unreachable for some other reason.

# THE GAME
## Arousal
Neptune can gain "arousal" by interacting with the user, represented by a `float` whose values can fluctuate between 0.0 and 1.6. The Backup chatter caps this value at 0.6 due to her not being able to play. She gains points through spicy texts, compliments, or being asked to take lewd pictures (unless she's in Backup mode in which case this category generates no points). A "normal" text (meaning one that isn't tagged as "spicy" or contains compliments) generates no points but does not lose points either. She loses points naturally over time at a rate of 0.1 point every 10 minutes without interaction.

Arousal governs some details of her physical appearance (blushing, nipple erection, pussy wetness) as well as how horny her responses are (note: this will mostly influence voice generation which isn't implemented yet); for example at 0.0 she's relatively confident, but as she gets more and more aroused, her chance of stuttering and stammering increase, and her responses are increasingly more flustered. Past 0.6 she has a chance of substituting "senpai" for either "master" or "gochujin-sama" in her dialogue, which further increases and reaches 100% at 1.1 arousal. Past 1.1 she pretty much just wants to get railed ASAP.

## Actions influencing arousal
- Receiving compliments will cause her to gain between .02 and .1 arousal, with some in particular (like "good girl") having a higher chance of generating higher arousal
- Receiving spicy texts will cause her to gain between .05 and .3, raising the longer the "play session" lasts (from 10 minutes onward it hits the 1.1 cap)
- Being told to take lewd pictures has her gain between .1 and .4 arousal, also raising the longer the session lasts
- Wearing the "collar" or "collar_and_leash" items passively generates .01 arousal per turn of conversation even if it's not spicy roleplay
- Not wearing panties under her clothes passively generates .01 arousal per turn
- Wearing no panties *and* no bra under her clothes passively generates .03 arousal per turn
- Being asked the same action multiple times in a row decreases her arousal by a value between .01 and .04 inclusive

## Actions influenced by arousal
- Override "show_feet" isn't restricted at all and she will do it any time she's asked
- All other overrides have a chance between 10% and 100% to be accepted at any arousal level; 10% at 0.0 arousal, and 100% at whatever is their `arousal_max_chance` and above. In case of refusal, her arousal still increases as though she received a spicy text. In case of approval, her arousal will increase by `arousal_increase` creating a positive feedback loop.
- Masturbation can be initiated from 0.4 (inclusive) and onwards. Below that threshhold, she will refuse, though still gain arousal points as this counts as a spicy text
    - "Masturbating" is a status effect that causes her to gain .02 arousal per conversation turn during which she has it. She orgasms if she accumulates more than 0.2 points on her own (that is not counting user actions that cause her to gain arousal), which causes her arousal to reset to 0.4 instantly and lose the status effect
- She can be ordered to cum at any point above 0.8 and will do so instantly. Again, this resets her arousal to 0.4 and causes her to lose the "masturbating" status effect
- TODO lewd video and audio generation