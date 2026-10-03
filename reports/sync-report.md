## Vocab sync

First sync: this run sets the baseline snapshot, so every row counts as existing (no new/changed/removed list).

|  | count |
|---|---|
| cards in app | 653 |
| new rows | 0 |
| changed rows (need reconciliation) | 0 |
| removed rows | 0 |
| blocked rows (validation errors) | 4 |
| duplicate rows | 2 exact, 0 conflicting, 0 same-hanzi |
| proposed sheet edits | 714 |
| cards reviewed by Claude | 657/653 (0 this run) |

> **Review:** no card content changed; nothing to review.

### How to use this PR
- **Sheet changes** (new / changed / removed) already happened in the Google Sheet. If one is wrong, fix it in the sheet; the next sync updates this PR.
- **Proposed sheet edits** are in `data/sheet_edits.json`. To reject one, set its `"status"` to `"rejected"` (edit the file in this PR). Rejected edits are never proposed again.
- **Merging** writes every remaining `proposed` edit back to the Google Sheet, then deploys the app.
- A card whose hanzi/pinyin/english/type changed gets a new id. The old id is kept as an alias, so study progress follows it.

### Blocked rows: fix in the sheet
These rows are left out of the app until fixed.

| tab | row | hanzi | field | problem |
|---|---|---|---|---|
| Activities | 62 | 健身 | english | required field is empty |
| Activities | 62 | 健身 | type | required field is empty |
| Directions | 55 | 急转 | english | required field is empty |
| Directions | 55 | 急转 | type | required field is empty |
| Transition Words | 82 | 才 | type | required field is empty |
| Transition Words | 83 | 又 | type | required field is empty |

### Duplicates within a tab

| tab | hanzi | rows | action |
|---|---|---|---|
| Activities | 健身 | 46, 62 | partial copy: row 62 will be removed |
| Directions | 急转 | 54, 55 | partial copy: row 55 will be removed |

### Proposed sheet edits

| key | status | tab | row | hanzi | field | before | after | conf. | why |
|---|---|---|---|---|---|---|---|---|---|
| 44555c602e51 | proposed | Activities | 62 | 健身 | * | · | (remove row) | · | partial copy of row 46 |
| 3f2c91e68225 | proposed | Directions | 55 | 急转 | * | · | (remove row) | · | partial copy of row 54 |
| d0f6439b01bd | proposed | Transition Words | 59 | 而且 | examples | · | 这个餐厅很便宜,而且很好吃。 \| Zhège cāntīng hěn piányi, érqiě hěn hǎochī. \| This restaurant is cheap, and the food is good too. | · | generated example sentence (uses only app vocab + allowed words) |
| f2e1bb657c1b | proposed | Body | 60 | 饿 | examples | · | 我饿了。 \| Wǒ è le. \| I'm hungry. | · | generated example sentence (uses only app vocab + allowed words) |
| 73b60e78779e | proposed | Activities | 33 | 做晚饭 | examples | · | 今天晚上我做晚饭。 \| Jīntiān wǎnshang wǒ zuò wǎnfàn. \| I'm cooking dinner tonight. | · | generated example sentence (uses only app vocab + allowed words) |
| d6cb487edfc8 | proposed | Body | 42 | 脖子 | measure_word | · | 个 (gè) | medium | 脖子 has no special measure word; the general 个 is used when one is needed. |
| 268c8acdd28f | proposed | Body | 42 | 脖子 | examples | · | 她的脖子很长。 \| Tā de bózi hěn cháng. \| She has a long neck. | · | generated example sentence (uses only app vocab + allowed words) |
| 2a5fb8b0d5ad | proposed | Familiar People | 39 | 室友 | examples | · | 我的室友很吵。 \| Wǒ de shìyǒu hěn chǎo. \| My roommate is very noisy. | · | generated example sentence (uses only app vocab + allowed words) |
| ebee366872a3 | proposed | Descriptions | 72 | 安静 | examples | · | 图书馆很安静。 \| Túshūguǎn hěn ānjìng. \| The library is quiet. | · | generated example sentence (uses only app vocab + allowed words) |
| b2220a632472 | proposed | Directions | 20 | 这里 | examples | · | 这里有一个超市。 \| Zhèlǐ yǒu yí ge chāoshì. \| There's a grocery store here. | · | generated example sentence (uses only app vocab + allowed words) |
| 60c8ad24b7f9 | proposed | Places | 7 | 银行 | examples | · | 银行在超市对面。 \| Yínháng zài chāoshì duìmiàn. \| The bank is across from the grocery store. | · | generated example sentence (uses only app vocab + allowed words) |
| ce0871433821 | proposed | Daily Life | 19 | 我没听懂 | examples | · | 不好意思，我没听懂。 \| Bù hǎoyìsi, wǒ méi tīngdǒng. \| Sorry, I didn't understand. | · | generated example sentence (uses only app vocab + allowed words) |
| d1d449bbf866 | proposed | Transition Words | 44 | 怎么说呢 | examples | · | 怎么说呢，这个电影有点儿奇怪。 \| Zěnme shuō ne, zhège diànyǐng yǒudiǎnr qíguài. \| How should I put it... this movie is a bit strange. | · | generated example sentence (uses only app vocab + allowed words) |
| e48ba4eb46dc | proposed | Transition Words | 28 | 小的时候 | examples | · | 小的时候我常常去公园。 \| Xiǎo de shíhou wǒ chángcháng qù gōngyuán. \| When I was little, I often went to the park. | · | generated example sentence (uses only app vocab + allowed words) |
| dbeac3f524d1 | proposed | Directions | 10 | 拐角 | measure_word | · | 个 (gè) | medium | Standard measure word for 拐角. |
| 5167045c3d17 | proposed | Directions | 10 | 拐角 | examples | · | 药店在拐角。 \| Yàodiàn zài guǎijiǎo. \| The pharmacy is at the corner. | · | generated example sentence (uses only app vocab + allowed words) |
| d54cfd4b4952 | proposed | Daily Life | 83 | 试 | examples | · | 我想试这件衣服。 \| wǒ xiǎng shì zhè jiàn yīfu. \| I'd like to try on this piece of clothing. | · | generated example sentence (uses only app vocab + allowed words) |
| 5ef707cdd96f | proposed | Daily Life | 79 | 想 | examples | · | 我想去公园。 \| wǒ xiǎng qù gōngyuán. \| I want to go to the park. | · | generated example sentence (uses only app vocab + allowed words) |
| 50360cd4978f | proposed | Familiar People | 42 | 前任 | examples | · | 我的前任是律师。 \| Wǒ de qiánrèn shì lǜshī. \| My ex is a lawyer. | · | generated example sentence (uses only app vocab + allowed words) |
| 1925795e6006 | proposed | Transition Words | 37 | 所以 | examples | · | 今天下雨，所以我不去公园了。 \| Jīntiān xiàyǔ, suǒyǐ wǒ bú qù gōngyuán le. \| It's raining today, so I'm not going to the park. | · | generated example sentence (uses only app vocab + allowed words) |
| c3ada1eb07c3 | proposed | Body | 52 | 肚子疼 | english | stomachache | to have a stomachache / stomachache | low | The type is adjective, and 肚子疼 is used predicatively (我肚子疼). A noun-only gloss doesn't match how the word works. |
| 0ae915b93c67 | proposed | Body | 52 | 肚子疼 | examples | · | 我肚子疼，要去医院看病。 \| Wǒ dùzi téng, yào qù yīyuàn kànbìng. \| I have a stomachache and need to go to the hospital to see a doctor. | · | generated example sentence (uses only app vocab + allowed words) |
| 6ff3b9afd785 | proposed | Activities | 30 | 住 | examples | · | 我住在市中心。 \| Wǒ zhù zài shìzhōngxīn. \| I live downtown. | · | generated example sentence (uses only app vocab + allowed words) |
| ff22de215c5e | proposed | Transition Words | 22 | 几次 | examples | · | 我去过那个博物馆几次。 \| Wǒ qù guo nàge bówùguǎn jǐ cì. \| I've been to that museum a few times. | · | generated example sentence (uses only app vocab + allowed words) |
| 065671ab35c9 | proposed | Daily Life | 28 | 午饭 | examples | · | 今天的午饭很好吃。 \| Jīntiān de wǔfàn hěn hǎochī. \| Today's lunch is really tasty. | · | generated example sentence (uses only app vocab + allowed words) |
| 36cdc2f1c208 | proposed | Familiar People | 13 | 单身 | examples | · | 我现在单身。 \| Wǒ xiànzài dānshēn. \| I'm single right now. | · | generated example sentence (uses only app vocab + allowed words) |
| 2ac593fb196b | proposed | Transition Words | 66 | 特别是 | examples | · | 我经常运动,特别是跑步。 \| Wǒ jīngcháng yùndòng, tèbié shì pǎobù. \| I exercise often, especially running. | · | generated example sentence (uses only app vocab + allowed words) |
| 37e88dcad9a6 | proposed | Directions | 31 | 北 | examples | · | 火车站在北边。 \| Huǒchēzhàn zài běibian. \| The train station is on the north side. | · | generated example sentence (uses only app vocab + allowed words) |
| 2fa434abfbea | proposed | Professional | 18 | 讲话 | english | to give a speech / talk at people | to give a talk / to speak (to a group) | low | "Talk at people" suggests lecturing or condescension, which 讲话 does not carry; it is a neutral word for speaking or addressing a group. |
| e1b616ad0c28 | proposed | Activities | 10 | 讲话 | english | to give a speech / talk at people | to give a talk / to speak (to a group) | low | "Talk at people" suggests lecturing or condescension, which 讲话 does not carry; it is a neutral word for speaking or addressing a group. |
| 97ecaaa6fbf1 | proposed | Professional | 18 | 讲话 | examples | · | 老板要讲话了。 \| Lǎobǎn yào jiǎnghuà le. \| The boss is about to give a talk. | · | generated example sentence (uses only app vocab + allowed words) |
| e8725fbec25f | proposed | Descriptions | 5 | 厉害 | examples | · | 你真厉害！ \| Nǐ zhēn lìhai! \| You're amazing! | · | generated example sentence (uses only app vocab + allowed words) |
| e68a3c3689a7 | proposed | Body | 50 | 感冒 | examples | · | 我感冒了，要吃药。 \| Wǒ gǎnmào le, yào chī yào. \| I've caught a cold and need to take medicine. | · | generated example sentence (uses only app vocab + allowed words) |
| 8476dd4bc468 | proposed | Descriptions | 79 | 苦 | examples | · | 这杯咖啡很苦。 \| Zhè bēi kāfēi hěn kǔ. \| This cup of coffee is very bitter. | · | generated example sentence (uses only app vocab + allowed words) |
| 30dfcbdd5778 | proposed | Transition Words | 73 | 为了 | type | conjunction | preposition | low | 为了 is normally classed as a preposition (介词) that introduces a purpose phrase, as in 为了省钱. |
| ec595f435b80 | proposed | Transition Words | 73 | 为了 | examples | · | 为了健身，我经常跑步。 \| wèile jiànshēn, wǒ jīngcháng pǎobù. \| To stay fit, I often go running. | · | generated example sentence (uses only app vocab + allowed words) |
| 5be6859baea4 | proposed | Directions | 39 | 迷路 | examples | · | 我在市中心迷路了。 \| Wǒ zài shìzhōngxīn mílù le. \| I got lost downtown. | · | generated example sentence (uses only app vocab + allowed words) |
| 4d787b568756 | proposed | Directions | 17 | 前 | examples | · | 楼前有一个公园。 \| Lóu qián yǒu yí ge gōngyuán. \| There's a park in front of the building. | · | generated example sentence (uses only app vocab + allowed words) |
| 6fb412a4a6a7 | proposed | Objects | 31 | 电影 | examples | · | 这个电影很有意思。 \| zhège diànyǐng hěn yǒu yìsi. \| This movie is very interesting. | · | generated example sentence (uses only app vocab + allowed words) |
| 23c172526a96 | proposed | Places | 53 | 学校 | examples | · | 我的学校离家很近。 \| wǒ de xuéxiào lí jiā hěn jìn. \| My school is very close to home. | · | generated example sentence (uses only app vocab + allowed words) |
| 624b59ef34a4 | proposed | Body | 26 | 疼 | examples | · | 我的头很疼。 \| Wǒ de tóu hěn téng. \| My head really hurts. | · | generated example sentence (uses only app vocab + allowed words) |
| bff124264c9e | proposed | Daily Life | 21 | 我听说 | examples | · | 我听说那家餐厅很好吃。 \| Wǒ tīngshuō nà jiā cāntīng hěn hǎochī. \| I heard that restaurant is really good. | · | generated example sentence (uses only app vocab + allowed words) |
| 072214fb3d6d | proposed | Directions | 46 | 走路 | examples | · | 我走路去学校。 \| Wǒ zǒulù qù xuéxiào. \| I walk to school. | · | generated example sentence (uses only app vocab + allowed words) |
| c573084c059c | proposed | Directions | 16 | 从 | examples | · | 从我家到公司要一个小时。 \| Cóng wǒ jiā dào gōngsī yào yí ge xiǎoshí. \| It takes an hour to get from my home to the office. | · | generated example sentence (uses only app vocab + allowed words) |
| 87dc5a3767d2 | proposed | Familiar People | 31 | 弟弟 | examples | · | 我弟弟很可爱。 \| wǒ dìdi hěn kě'ài. \| My younger brother is very cute. | · | generated example sentence (uses only app vocab + allowed words) |
| 52d332b8f715 | proposed | Professional | 29 | 项目 | examples | · | 这个项目很重要。 \| Zhège xiàngmù hěn zhòngyào. \| This project is very important. | · | generated example sentence (uses only app vocab + allowed words) |
| c20ce69489c7 | proposed | Transition Words | 75 | 可能 | type | phrase | adverb | medium | 可能 is a single word. It is mainly used as an adverb ('maybe/probably') or as an adjective ('possible'), not as a phrase. |
| 2f516b9154de | proposed | Transition Words | 75 | 可能 | examples | · | 明天可能下雨。 \| míngtiān kěnéng xiàyǔ. \| It might rain tomorrow. | · | generated example sentence (uses only app vocab + allowed words) |
| be421f32052b | proposed | Familiar People | 38 | 邻居 | examples | · | 我的邻居有一只猫。 \| Wǒ de línjū yǒu yì zhī māo. \| My neighbor has a cat. | · | generated example sentence (uses only app vocab + allowed words) |
| acc359ed7e49 | proposed | Food | 2 | 吃法 | measure_word | · | 种 (zhǒng) | high | 吃法 is counted with 种 (kinds/ways), e.g. 三种吃法. |
| 782a139e3804 | proposed | Food | 2 | 吃法 | examples | · | 这个吃法很简单。 \| zhège chīfǎ hěn jiǎndān. \| This way of eating it is simple. | · | generated example sentence (uses only app vocab + allowed words) |
| 660e26a050bb | proposed | Professional | 25 | 数据工程师 | examples | · | 我姐姐是数据工程师。 \| Wǒ jiějie shì shùjù gōngchéngshī. \| My older sister is a data engineer. | · | generated example sentence (uses only app vocab + allowed words) |
| 0a77d08f4a73 | proposed | Places | 26 | 超市 | examples | · | 我去超市买水果。 \| Wǒ qù chāoshì mǎi shuǐguǒ. \| I'm going to the grocery store to buy fruit. | · | generated example sentence (uses only app vocab + allowed words) |
| a5022b1adb9c | proposed | Professional | 12 | 请假 | examples | · | 我明天要请假。 \| Wǒ míngtiān yào qǐngjià. \| I need to ask for time off tomorrow. | · | generated example sentence (uses only app vocab + allowed words) |
| 22a9478ecacb | proposed | Directions | 28 | 英里 | examples | · | 这里离机场十英里。 \| Zhèlǐ lí jīchǎng shí yīnglǐ. \| It's ten miles from here to the airport. | · | generated example sentence (uses only app vocab + allowed words) |
| 6e3afdbc4eb7 | proposed | Familiar People | 47 | 咱们 | examples | · | 咱们去吃饭吧。 \| Zánmen qù chīfàn ba. \| Let's go eat. | · | generated example sentence (uses only app vocab + allowed words) |
| a5bffc9c0c1b | proposed | Daily Life | 81 | 收拾 | examples | · | 我在收拾卧室。 \| wǒ zài shōushi wòshì. \| I'm tidying up the bedroom. | · | generated example sentence (uses only app vocab + allowed words) |
| 11928070d897 | proposed | Daily Life | 95 | 你说得对 | examples | · | 你说得对，这个太贵了。 \| nǐ shuō de duì, zhège tài guì le. \| You're right, this is too expensive. | · | generated example sentence (uses only app vocab + allowed words) |
| 9b8b4c525daf | proposed | Descriptions | 36 | 浅紫色 | examples | · | 妹妹想买浅紫色的雨伞。 \| mèimei xiǎng mǎi qiǎn zǐsè de yǔsǎn. \| My little sister wants to buy a lavender umbrella. | · | generated example sentence (uses only app vocab + allowed words) |
| a8b940d24fab | proposed | Body | 55 | 受伤 | examples | · | 他受伤了。 \| Tā shòushāng le. \| He got hurt. | · | generated example sentence (uses only app vocab + allowed words) |
| ebf60f349381 | proposed | Daily Life | 60 | 回家 | examples | · | 我下班以后回家。 \| Wǒ xiàbān yǐhòu huíjiā. \| I go home after I get off work. | · | generated example sentence (uses only app vocab + allowed words) |
| 383a28a2acb3 | proposed | Daily Life | 3 | 几乎不 | examples | · | 我几乎不喝咖啡。 \| wǒ jīhū bù hē kāfēi. \| I almost never drink coffee. | · | generated example sentence (uses only app vocab + allowed words) |
| 42c021d73505 | proposed | Transition Words | 64 | 也就是说 | examples | · | 他明天休假,也就是说他不上班。 \| Tā míngtiān xiūjià, yě jiù shì shuō tā bú shàngbān. \| He's off tomorrow, which means he isn't going to work. | · | generated example sentence (uses only app vocab + allowed words) |
| 0683d48ccd62 | proposed | Transition Words | 16 | 以后 | examples | · | 吃饭以后我们去散步吧。 \| Chīfàn yǐhòu wǒmen qù sànbù ba. \| Let's go for a walk after we eat. | · | generated example sentence (uses only app vocab + allowed words) |
| dc614e952b63 | proposed | Daily Life | 64 | 安排 | examples | · | 你周末有什么安排？ \| Nǐ zhōumò yǒu shénme ānpái? \| What are your plans for the weekend? | · | generated example sentence (uses only app vocab + allowed words) |
| c0a5c4646168 | proposed | Transition Words | 53 | 给 | examples | · | 妈妈给我一本书。 \| Māma gěi wǒ yì běn shū. \| Mom gave me a book. | · | generated example sentence (uses only app vocab + allowed words) |
| 399d87ef6a1b | proposed | Activities | 54 | 卖 | examples | · | 这家店卖什么？ \| zhè jiā diàn mài shénme? \| What does this shop sell? | · | generated example sentence (uses only app vocab + allowed words) |
| 734917775bf2 | proposed | Transition Words | 58 | 虽然 | examples | · | 虽然很贵,但是很好吃。 \| Suīrán hěn guì, dànshì hěn hǎochī. \| Although it's expensive, it's delicious. | · | generated example sentence (uses only app vocab + allowed words) |
| f4facaa317c8 | proposed | Familiar People | 7 | 家人 | examples | · | 周末我跟家人吃饭。 \| Zhōumò wǒ gēn jiārén chīfàn. \| I have meals with my family on weekends. | · | generated example sentence (uses only app vocab + allowed words) |
| 78d6a0a77958 | proposed | Body | 9 | 我不太舒服 | examples | · | 我不太舒服，我要回家。 \| wǒ bú tài shūfu, wǒ yào huíjiā. \| I don't feel well, I want to go home. | · | generated example sentence (uses only app vocab + allowed words) |
| 01bb1872740c | proposed | Descriptions | 87 | 酷 | examples | · | 你的车真酷！ \| nǐ de chē zhēn kù! \| Your car is so cool! | · | generated example sentence (uses only app vocab + allowed words) |
| c8957a150af2 | proposed | Objects | 28 | 钥匙 | examples | · | 我的钥匙在哪儿？ \| Wǒ de yàoshi zài nǎr? \| Where are my keys? | · | generated example sentence (uses only app vocab + allowed words) |
| a4a92ed63319 | proposed | Professional | 31 | 下班 | examples | · | 你几点下班？ \| nǐ jǐ diǎn xiàbān? \| What time do you get off work? | · | generated example sentence (uses only app vocab + allowed words) |
| 3b26f9b638fd | proposed | Descriptions | 11 | 热 | examples | · | 这里太热了。 \| Zhèlǐ tài rè le. \| It's too hot here. | · | generated example sentence (uses only app vocab + allowed words) |
| e4e97e601497 | proposed | Places | 36 | 厨房 | examples | · | 我家的厨房很小。 \| wǒ jiā de chúfáng hěn xiǎo. \| The kitchen in my home is very small. | · | generated example sentence (uses only app vocab + allowed words) |
| df4f71f50cd4 | proposed | Activities | 39 | 跑步 | examples | · | 我早上常常跑步。 \| wǒ zǎoshang chángcháng pǎobù. \| I often go running in the morning. | · | generated example sentence (uses only app vocab + allowed words) |
| b4838459877e | proposed | Transition Words | 8 | 每隔 | english | every other | every (at intervals of) | low | 每隔 means 'at intervals of'. Only 每隔一天 gives 'every other day'; 每隔两天 means every three days, and 每隔半个小时 means every half hour. |
| 5e0209bfebc6 | proposed | Transition Words | 8 | 每隔 | examples | · | 他每隔半个小时看一次手机。 \| tā měi gé bàn ge xiǎoshí kàn yí cì shǒujī. \| He checks his phone every half hour. | · | generated example sentence (uses only app vocab + allowed words) |
| d7d10c674a28 | proposed | Places | 9 | 浴室 | examples | · | 浴室在卧室旁边。 \| Yùshì zài wòshì pángbiān. \| The bathroom is next to the bedroom. | · | generated example sentence (uses only app vocab + allowed words) |
| e250f7a52318 | proposed | Familiar People | 30 | 哥哥 | examples | · | 我哥哥比我高。 \| wǒ gēge bǐ wǒ gāo. \| My older brother is taller than me. | · | generated example sentence (uses only app vocab + allowed words) |
| 61d138752c05 | proposed | Transition Words | 46 | 不到 | examples | · | 我家离公司很近，走路不到半个小时。 \| Wǒ jiā lí gōngsī hěn jìn, zǒulù búdào bàn ge xiǎoshí. \| My home is close to the office; it's less than half an hour on foot. | · | generated example sentence (uses only app vocab + allowed words) |
| 005a0e7faebd | proposed | Directions | 13 | 楼下 | examples | · | 我在楼下等你。 \| Wǒ zài lóuxià děng nǐ. \| I'm waiting for you downstairs. | · | generated example sentence (uses only app vocab + allowed words) |
| d64c99352a04 | proposed | Activities | 43 | 看书 | examples | · | 我在图书馆看书。 \| wǒ zài túshūguǎn kànshū. \| I'm reading at the library. | · | generated example sentence (uses only app vocab + allowed words) |
| 0f1270512d09 | proposed | Directions | 23 | 中间 | examples | · | 银行在超市和书店中间。 \| Yínháng zài chāoshì hé shūdiàn zhōngjiān. \| The bank is between the grocery store and the bookstore. | · | generated example sentence (uses only app vocab + allowed words) |
| 61ccd07dc897 | proposed | Directions | 34 | 右 | examples | · | 地铁站在右边。 \| Dìtiězhàn zài yòubian. \| The subway station is on the right. | · | generated example sentence (uses only app vocab + allowed words) |
| b28e642953ee | proposed | Directions | 37 | 那里 | examples | · | 我的包在那里。 \| Wǒ de bāo zài nàlǐ. \| My bag is over there. | · | generated example sentence (uses only app vocab + allowed words) |
| 4d9de35cea0c | proposed | Daily Life | 49 | 带 | examples | · | 下雨了，你带雨伞吧。 \| xiàyǔ le, nǐ dài yǔsǎn ba. \| It's raining, take an umbrella. | · | generated example sentence (uses only app vocab + allowed words) |
| 279fb383e189 | proposed | Body | 31 | 心情 | measure_word | · | 种 (zhǒng) | low | Noun card with no measure word. 心情 is seldom counted, but 种 ("a kind of mood") is the usual one when it is. |
| 0c22cba23a8f | proposed | Body | 31 | 心情 | examples | · | 今天我的心情很好。 \| Jīntiān wǒ de xīnqíng hěn hǎo. \| I'm in a really good mood today. | · | generated example sentence (uses only app vocab + allowed words) |
| ccc49a3a3fe5 | proposed | Descriptions | 82 | 重要 | examples | · | 这个会议很重要。 \| Zhège huìyì hěn zhòngyào. \| This meeting is very important. | · | generated example sentence (uses only app vocab + allowed words) |
| c2557363fd28 | proposed | Directions | 47 | 往 | examples | · | 你往前直走。 \| Nǐ wǎng qián zhí zǒu. \| Go straight ahead. | · | generated example sentence (uses only app vocab + allowed words) |
| fea3378e8caf | proposed | Daily Life | 58 | 送 | examples | · | 我送你回家吧。 \| Wǒ sòng nǐ huíjiā ba. \| Let me take you home. | · | generated example sentence (uses only app vocab + allowed words) |
| 95327c7b4fc2 | proposed | Activities | 6 | 度假 | type | verb | VOV | medium | 度假 is a separable verb-object compound (度 + 假, e.g. 度了一个假), consistent with how 受伤/减肥 are typed. |
| 4a9c7e406b6a | proposed | Activities | 6 | 度假 | examples | · | 我们去国外度假了。 \| Wǒmen qù guówài dùjià le. \| We went abroad on vacation. | · | generated example sentence (uses only app vocab + allowed words) |
| 6f5d4be5d7c1 | proposed | Places | 22 | 乡下 | examples | · | 我奶奶住在乡下。 \| Wǒ nǎinai zhù zài xiāngxia. \| My grandma lives in the countryside. | · | generated example sentence (uses only app vocab + allowed words) |
| 48a29cc32d8a | proposed | Body | 15 | 刷牙 | examples | · | 我早上起床就刷牙。 \| Wǒ zǎoshang qǐchuáng jiù shuā yá. \| I brush my teeth as soon as I get up in the morning. | · | generated example sentence (uses only app vocab + allowed words) |
| a228369c8909 | proposed | Places | 31 | 老家 | examples | · | 你老家在哪儿？ \| Nǐ lǎojiā zài nǎr? \| Where is your hometown? | · | generated example sentence (uses only app vocab + allowed words) |
| 7b6e9a0876d2 | proposed | Directions | 41 | 坐 | examples | · | 我坐地铁去公司。 \| Wǒ zuò dìtiě qù gōngsī. \| I take the subway to the office. | · | generated example sentence (uses only app vocab + allowed words) |
| 9902c2f358b4 | proposed | Objects | 21 | 电梯 | examples | · | 这个电梯坏了。 \| Zhège diàntī huài le. \| This elevator is broken. | · | generated example sentence (uses only app vocab + allowed words) |
| ea094198a632 | proposed | Transition Words | 61 | 其实 | type | phrase | adverb | medium | 其实 is a single-word sentence adverb (actually / in fact), not a phrase. |
| 91c78e845826 | proposed | Transition Words | 61 | 其实 | examples | · | 其实我不累。 \| Qíshí wǒ bú lèi. \| Actually, I'm not tired. | · | generated example sentence (uses only app vocab + allowed words) |
| b8e8d3dd3913 | proposed | Daily Life | 16 | 我看不见 | examples | · | 你在哪儿？我看不见你。 \| Nǐ zài nǎr? Wǒ kàn bu jiàn nǐ. \| Where are you? I can't see you. | · | generated example sentence (uses only app vocab + allowed words) |
| 549f763a991b | proposed | Professional | 40 | 职场 | examples | · | 职场很复杂。 \| zhíchǎng hěn fùzá. \| The working world is complicated. | · | generated example sentence (uses only app vocab + allowed words) |
| 4ae34d76a8b1 | proposed | Places | 18 | 中餐馆 | examples | · | 我们去中餐馆吃饭吧。 \| Wǒmen qù zhōngcānguǎn chīfàn ba. \| Let's go eat at a Chinese restaurant. | · | generated example sentence (uses only app vocab + allowed words) |
| ffc9fe793102 | proposed | Familiar People | 45 | 在一起 | examples | · | 他们已经在一起了。 \| Tāmen yǐjīng zài yìqǐ le. \| They're already together. | · | generated example sentence (uses only app vocab + allowed words) |
| e388cde123e8 | proposed | Familiar People | 6 | 女儿 | examples | · | 他们的女儿很可爱。 \| Tāmen de nǚ'ér hěn kě'ài. \| Their daughter is very cute. | · | generated example sentence (uses only app vocab + allowed words) |
| 597d8437d090 | proposed | Places | 2 | 国外 | examples | · | 我哥哥在国外工作。 \| Wǒ gēge zài guówài gōngzuò. \| My older brother works abroad. | · | generated example sentence (uses only app vocab + allowed words) |
| fba28ff7bb1f | proposed | Transition Words | 56 | 我想 / 我要 | examples | · | 我想喝咖啡。 \| Wǒ xiǎng hē kāfēi. \| I'd like to drink some coffee. | · | generated example sentence (uses only app vocab + allowed words) |
| a124049b7e17 | proposed | Descriptions | 7 | 坏 | english | broken | bad / broken | medium | 坏 primarily means 'bad'; 'broken' is mainly its sense in 坏了. A gloss of only 'broken' hides the core meaning. |
| e03f9e1b3f1e | proposed | Descriptions | 7 | 坏 | examples | · | 我的手机坏了。 \| Wǒ de shǒujī huài le. \| My phone is broken. | · | generated example sentence (uses only app vocab + allowed words) |
| 858149544e17 | proposed | Descriptions | 74 | 舒服 | examples | · | 这把椅子很舒服。 \| Zhè bǎ yǐzi hěn shūfu. \| This chair is very comfortable. | · | generated example sentence (uses only app vocab + allowed words) |
| bf2360ab1385 | proposed | Professional | 39 | 汇报 | english | to report to / hand in | to report (to a superior) | medium | 汇报 means to report on work/progress to a superior; "hand in" (submit something) is 交, not 汇报. |
| 852a571fd31b | proposed | Professional | 39 | 汇报 | examples | · | 我明天要跟老板汇报。 \| wǒ míngtiān yào gēn lǎobǎn huìbào. \| I have to report to my boss tomorrow. | · | generated example sentence (uses only app vocab + allowed words) |
| f0fab6426c32 | proposed | Places | 37 | 大楼 | measure_word | 个 (gè) | 栋 (dòng) | low | 个 is acceptable, but 栋 (or 座) is the standard measure word for buildings, especially large ones. |
| 31aca7a917c6 | proposed | Places | 37 | 大楼 | examples | · | 那栋大楼很高。 \| nà dòng dàlóu hěn gāo. \| That building is very tall. | · | generated example sentence (uses only app vocab + allowed words) |
| c65d3235ff7e | proposed | Daily Life | 14 | 节日 | examples | · | 今天是节日，商场很热闹。 \| Jīntiān shì jiérì, shāngchǎng hěn rènao. \| Today is a holiday, so the mall is really lively. | · | generated example sentence (uses only app vocab + allowed words) |
| 5379b51c3a3c | proposed | Descriptions | 85 | 简单 | examples | · | 这个游戏很简单。 \| zhège yóuxì hěn jiǎndān. \| This game is simple. | · | generated example sentence (uses only app vocab + allowed words) |
| b2fae3a8b43d | proposed | Daily Life | 54 | 洗衣服 | examples | · | 我周末洗衣服。 \| wǒ zhōumò xǐ yīfu. \| I do laundry on weekends. | · | generated example sentence (uses only app vocab + allowed words) |
| f9073db76f08 | proposed | Places | 12 | 卧室 | examples | · | 我的卧室很小。 \| Wǒ de wòshì hěn xiǎo. \| My bedroom is small. | · | generated example sentence (uses only app vocab + allowed words) |
| 736262f9abf8 | proposed | Professional | 10 | 会议 | examples | · | 今天下午有一个会议。 \| Jīntiān xiàwǔ yǒu yí ge huìyì. \| There's a meeting this afternoon. | · | generated example sentence (uses only app vocab + allowed words) |
| 3574a7b71564 | proposed | Activities | 41 | 逛街 | examples | · | 周末我跟朋友去逛街。 \| zhōumò wǒ gēn péngyou qù guàngjiē. \| On the weekend I go shopping with friends. | · | generated example sentence (uses only app vocab + allowed words) |
| 50f8354dfe27 | proposed | Body | 11 | 好多了 | examples | · | 我今天好多了。 \| wǒ jīntiān hǎo duō le. \| I'm much better today. | · | generated example sentence (uses only app vocab + allowed words) |
| 06d25a4bcf98 | proposed | Descriptions | 70 | 短 | examples | · | 这条裤子太短了。 \| Zhè tiáo kùzi tài duǎn le. \| These pants are too short. | · | generated example sentence (uses only app vocab + allowed words) |
| 17a85186c073 | proposed | Daily Life | 27 | 我们改天吧 | examples | · | 我今天很忙，我们改天吧。 \| Wǒ jīntiān hěn máng, wǒmen gǎitiān ba. \| I'm really busy today, let's do another day. | · | generated example sentence (uses only app vocab + allowed words) |
| 8770efcde92e | proposed | Directions | 8 | 下面 | examples | · | 猫在床下面。 \| Māo zài chuáng xiàmiàn. \| The cat is under the bed. | · | generated example sentence (uses only app vocab + allowed words) |
| 2f8c239803b1 | proposed | Directions | 9 | 下 | examples | · | 猫在桌子下睡觉。 \| Māo zài zhuōzi xià shuìjiào. \| The cat is sleeping under the table. | · | generated example sentence (uses only app vocab + allowed words) |
| 7285d37f898a | proposed | Transition Words | 2 | 总是 | examples | · | 他总是迟到。 \| tā zǒngshì chídào. \| He's always late. | · | generated example sentence (uses only app vocab + allowed words) |
| aff33496028e | proposed | Daily Life | 84 | 明白 | examples | · | 我明白了。 \| wǒ míngbai le. \| Got it, I understand now. | · | generated example sentence (uses only app vocab + allowed words) |
| a793b11b60b0 | proposed | Places | 19 | 城市 | examples | · | 这个城市很热闹。 \| Zhège chéngshì hěn rènao. \| This city is very lively. | · | generated example sentence (uses only app vocab + allowed words) |
| 7a2e21f0f57e | proposed | Objects | 29 | 奶茶 | examples | · | 这杯奶茶太甜了。 \| Zhè bēi nǎichá tài tián le. \| This cup of milk tea is too sweet. | · | generated example sentence (uses only app vocab + allowed words) |
| 129707466833 | proposed | Familiar People | 24 | 朋友 | examples | · | 他是我的朋友。 \| tā shì wǒ de péngyou. \| He is my friend. | · | generated example sentence (uses only app vocab + allowed words) |
| c3042d054366 | proposed | Body | 44 | 脚 | examples | · | 我今天走路去公司，脚很疼。 \| Wǒ jīntiān zǒulù qù gōngsī, jiǎo hěn téng. \| I walked to the office today, and my feet really hurt. | · | generated example sentence (uses only app vocab + allowed words) |
| 4980df1a9798 | proposed | Places | 23 | 市中心 | examples | · | 我的公寓在市中心。 \| Wǒ de gōngyù zài shìzhōngxīn. \| My apartment is downtown. | · | generated example sentence (uses only app vocab + allowed words) |
| 20e003e2d685 | proposed | Activities | 19 | 尝 | examples | · | 我想尝你做的饺子。 \| Wǒ xiǎng cháng nǐ zuò de jiǎozi. \| I want to taste the dumplings you made. | · | generated example sentence (uses only app vocab + allowed words) |
| 4ec32ae787aa | proposed | Daily Life | 78 | 洗澡 | examples | · | 我跑步以后洗澡。 \| Wǒ pǎobù yǐhòu xǐzǎo. \| I take a shower after I run. | · | generated example sentence (uses only app vocab + allowed words) |
| 33824acff03f | proposed | Body | 27 | 头发 | examples | · | 她的头发很长。 \| Tā de tóufa hěn cháng. \| Her hair is very long. | · | generated example sentence (uses only app vocab + allowed words) |
| 8afb65d44e10 | proposed | Objects | 20 | 鸡蛋 | examples | · | 我买了两个鸡蛋。 \| Wǒ mǎi le liǎng ge jīdàn. \| I bought two eggs. | · | generated example sentence (uses only app vocab + allowed words) |
| 775d5746c607 | proposed | Directions | 50 | 哪里 | examples | · | 洗手间在哪里？ \| Xǐshǒujiān zài nǎlǐ? \| Where is the restroom? | · | generated example sentence (uses only app vocab + allowed words) |
| 53dc7065574a | proposed | Directions | 40 | 直走 | examples | · | 直走就到了。 \| Zhí zǒu jiù dào le. \| Go straight and you'll be there. | · | generated example sentence (uses only app vocab + allowed words) |
| fd325a1f5bce | proposed | Transition Words | 50 | 不一定 | examples | · | 贵的不一定好。 \| Guì de bù yídìng hǎo. \| Expensive things aren't necessarily good. | · | generated example sentence (uses only app vocab + allowed words) |
| f4d6f2f4bb69 | proposed | Objects | 4 | 一个小时 | examples | · | 我等了一个小时。 \| Wǒ děng le yí ge xiǎoshí. \| I waited for an hour. | · | generated example sentence (uses only app vocab + allowed words) |
| 0f0b3270a1ef | proposed | Activities | 51 | 打电话 | examples | · | 明天给我打电话吧。 \| míngtiān gěi wǒ dǎ diànhuà ba. \| Give me a call tomorrow. | · | generated example sentence (uses only app vocab + allowed words) |
| 4f63a5aaffaf | proposed | Activities | 28 | 脱衣服 | examples | · | 他到家以后就脱衣服洗澡。 \| Tā dào jiā yǐhòu jiù tuō yīfu xǐzǎo. \| As soon as he gets home, he takes off his clothes and showers. | · | generated example sentence (uses only app vocab + allowed words) |
| 11f3894da120 | proposed | Activities | 56 | 喝茶 | examples | · | 下午我们去喝茶吧。 \| xiàwǔ wǒmen qù hēchá ba. \| Let's go have tea this afternoon. | · | generated example sentence (uses only app vocab + allowed words) |
| 7c150ce56b4c | proposed | Food | 4 | 新鲜 | examples | · | 这个市场的蔬菜很新鲜。 \| zhège shìchǎng de shūcài hěn xīnxian. \| The vegetables at this market are very fresh. | · | generated example sentence (uses only app vocab + allowed words) |
| 95b63dab051c | proposed | Activities | 37 | 喝 | examples | · | 你要喝咖啡吗？ \| nǐ yào hē kāfēi ma? \| Do you want to drink some coffee? | · | generated example sentence (uses only app vocab + allowed words) |
| f63fa00773e4 | proposed | Professional | 23 | 经理 | examples | · | 我们的经理很忙。 \| Wǒmen de jīnglǐ hěn máng. \| Our manager is very busy. | · | generated example sentence (uses only app vocab + allowed words) |
| 090ab674273b | proposed | Places | 10 | 洗手间 | examples | · | 不好意思，洗手间在哪儿？ \| Bù hǎoyìsi, xǐshǒujiān zài nǎr? \| Excuse me, where is the restroom? | · | generated example sentence (uses only app vocab + allowed words) |
| 696827c073db | proposed | Daily Life | 4 | 纪念日 | examples | · | 明天是我们的纪念日。 \| míngtiān shì wǒmen de jìniànrì. \| Tomorrow is our anniversary. | · | generated example sentence (uses only app vocab + allowed words) |
| 9187c9db0bb0 | proposed | Transition Words | 20 | 下次 | examples | · | 下次我请客。 \| Xià cì wǒ qǐngkè. \| Next time it's on me. | · | generated example sentence (uses only app vocab + allowed words) |
| 2532da459a9b | proposed | Body | 14 | 出院 | examples | · | 我妈妈今天出院了。 \| Wǒ māma jīntiān chūyuàn le. \| My mom was discharged from the hospital today. | · | generated example sentence (uses only app vocab + allowed words) |
| 9540d864a06e | proposed | Descriptions | 61 | 难过 | examples | · | 他分手了，很难过。 \| Tā fēnshǒu le, hěn nánguò. \| He broke up and he's really sad. | · | generated example sentence (uses only app vocab + allowed words) |
| 0e2981ca7d91 | proposed | Familiar People | 28 | 爸爸 | examples | · | 我爸爸会开车。 \| wǒ bàba huì kāichē. \| My dad can drive. | · | generated example sentence (uses only app vocab + allowed words) |
| 1f565cb6bc5c | proposed | Descriptions | 52 | 旧 | examples | · | 我的电脑太旧了。 \| Wǒ de diànnǎo tài jiù le. \| My computer is too old. | · | generated example sentence (uses only app vocab + allowed words) |
| f6059fa06407 | proposed | Professional | 37 | 升职 | examples | · | 她升职了！ \| tā shēngzhí le! \| She got promoted! | · | generated example sentence (uses only app vocab + allowed words) |
| a49adcf2a151 | proposed | Descriptions | 54 | 贵 | examples | · | 这里的咖啡太贵了。 \| Zhèlǐ de kāfēi tài guì le. \| The coffee here is too expensive. | · | generated example sentence (uses only app vocab + allowed words) |
| 883808e0c6a2 | proposed | Activities | 5 | 爬山 | examples | · | 明天我们去爬山吧。 \| Míngtiān wǒmen qù páshān ba. \| Let's go hiking tomorrow. | · | generated example sentence (uses only app vocab + allowed words) |
| 7a2446a3d9c0 | proposed | Objects | 36 | 盘子 | examples | · | 这个盘子很干净。 \| zhège pánzi hěn gānjìng. \| This plate is clean. | · | generated example sentence (uses only app vocab + allowed words) |
| 3e4a130bedfb | proposed | Descriptions | 78 | 酸 | examples | · | 这个水果很酸。 \| Zhège shuǐguǒ hěn suān. \| This fruit is very sour. | · | generated example sentence (uses only app vocab + allowed words) |
| 9a9fcacf7391 | proposed | Familiar People | 14 | 心上人 | examples | · | 她是我的心上人。 \| Tā shì wǒ de xīnshàngrén. \| She's the one I love. | · | generated example sentence (uses only app vocab + allowed words) |
| 45bf2ff817d2 | proposed | Places | 41 | 市场 | examples | · | 这个市场的水果很新鲜。 \| zhège shìchǎng de shuǐguǒ hěn xīnxian. \| The fruit at this market is very fresh. | · | generated example sentence (uses only app vocab + allowed words) |
| ae52a5343213 | proposed | Body | 6 | 忌口 | examples | · | 你有什么忌口吗？ \| nǐ yǒu shénme jìkǒu ma? \| Is there anything you can't eat? | · | generated example sentence (uses only app vocab + allowed words) |
| 98e3d2e58849 | proposed | Descriptions | 43 | 红色 | examples | · | 我想买一个红色的包。 \| wǒ xiǎng mǎi yí ge hóngsè de bāo. \| I want to buy a red bag. | · | generated example sentence (uses only app vocab + allowed words) |
| 2cf37422db67 | proposed | Transition Words | 31 | 现在 | examples | · | 我现在很累。 \| Wǒ xiànzài hěn lèi. \| I'm really tired right now. | · | generated example sentence (uses only app vocab + allowed words) |
| 2f3303ec5859 | proposed | Objects | 5 | 包 | examples | · | 这个包很贵。 \| Zhège bāo hěn guì. \| This bag is very expensive. | · | generated example sentence (uses only app vocab + allowed words) |
| 75dec54a5384 | proposed | Activities | 7 | 庆祝 | examples | · | 我们去酒吧庆祝吧。 \| Wǒmen qù jiǔbā qìngzhù ba. \| Let's go to a bar to celebrate. | · | generated example sentence (uses only app vocab + allowed words) |
| 3987082ca267 | proposed | Daily Life | 93 | 那还好 | examples | · | 就一个小时？那还好。 \| jiù yí ge xiǎoshí? nà hái hǎo. \| Only an hour? Well, that's not so bad. | · | generated example sentence (uses only app vocab + allowed words) |
| f7c6ae66e74a | proposed | Daily Life | 94 | 现在几点 | examples | · | 不好意思，现在几点？ \| bù hǎoyìsi, xiànzài jǐ diǎn? \| Excuse me, what time is it? | · | generated example sentence (uses only app vocab + allowed words) |
| d55ec5d9b8d8 | proposed | Familiar People | 3 | 男朋友 | examples | · | 她有男朋友吗? \| Tā yǒu nán péngyou ma? \| Does she have a boyfriend? | · | generated example sentence (uses only app vocab + allowed words) |
| b2c5e6acee42 | proposed | Places | 33 | 酒店 | examples | · | 这家酒店很贵。 \| Zhè jiā jiǔdiàn hěn guì. \| This hotel is very expensive. | · | generated example sentence (uses only app vocab + allowed words) |
| 097994357edb | proposed | Descriptions | 4 | 左右 | examples | · | 我们等了一个小时左右。 \| Wǒmen děng le yí ge xiǎoshí zuǒyòu. \| We waited for about an hour. | · | generated example sentence (uses only app vocab + allowed words) |
| cf8d7fd1f3da | proposed | Transition Words | 36 | 只要 | english | if only / as long as | as long as / provided that | medium | English "if only" expresses a wish, as in "if only I had...". That is 要是……就好了, not 只要. 只要 means "as long as / provided that". |
| d5feca0c69ae | proposed | Transition Words | 36 | 只要 | examples | · | 只要你有空，我们就去看电影。 \| Zhǐyào nǐ yǒu kòng, wǒmen jiù qù kàn diànyǐng. \| As long as you're free, we'll go see a movie. | · | generated example sentence (uses only app vocab + allowed words) |
| 4a9445861dfc | proposed | Directions | 12 | 离 | examples | · | 超市离这里远吗？ \| Chāoshì lí zhèlǐ yuǎn ma? \| Is the grocery store far from here? | · | generated example sentence (uses only app vocab + allowed words) |
| 9ca1fce7f67f | proposed | Places | 4 | 公寓 | examples | · | 我租了一套公寓。 \| Wǒ zū le yí tào gōngyù. \| I rented an apartment. | · | generated example sentence (uses only app vocab + allowed words) |
| 4a357f71ac81 | proposed | Familiar People | 21 | 见面 | examples | · | 我们明天见面吧。 \| wǒmen míngtiān jiànmiàn ba. \| Let's meet up tomorrow. | · | generated example sentence (uses only app vocab + allowed words) |
| d2f614541681 | proposed | Places | 8 | 酒吧 | examples | · | 周末我们去酒吧喝啤酒。 \| Zhōumò wǒmen qù jiǔbā hē píjiǔ. \| On the weekend we go to a bar to drink beer. | · | generated example sentence (uses only app vocab + allowed words) |
| 23ab0a89935e | proposed | Descriptions | 27 | 深蓝色 | examples | · | 我想买一条深蓝色的裤子。 \| wǒ xiǎng mǎi yì tiáo shēn lánsè de kùzi. \| I want to buy a pair of navy pants. | · | generated example sentence (uses only app vocab + allowed words) |
| 9fc6de7d9bb7 | proposed | Familiar People | 4 | 男性朋友 | examples | · | 他是我的男性朋友,不是我男朋友。 \| Tā shì wǒ de nánxìng péngyou, bú shì wǒ nán péngyou. \| He's a male friend of mine, not my boyfriend. | · | generated example sentence (uses only app vocab + allowed words) |
| 8e6f1205f3c1 | proposed | Professional | 19 | 开会 | examples | · | 我们明天下午开会。 \| Wǒmen míngtiān xiàwǔ kāihuì. \| We have a meeting tomorrow afternoon. | · | generated example sentence (uses only app vocab + allowed words) |
| c328f1b15b04 | proposed | Objects | 55 | 水 | examples | · | 我要一杯水。 \| Wǒ yào yì bēi shuǐ. \| I'd like a glass of water. | · | generated example sentence (uses only app vocab + allowed words) |
| e2e7a4434a90 | proposed | Body | 53 | 嗓子疼 | type | adjective | phrase | medium | 嗓子疼 is a subject + predicate phrase (throat + hurts), not a single adjective. |
| 099187dd4416 | proposed | Body | 53 | 嗓子疼 | examples | · | 我今天嗓子疼。 \| Wǒ jīntiān sǎngzi téng. \| I have a sore throat today. | · | generated example sentence (uses only app vocab + allowed words) |
| 22bd531fb876 | proposed | Directions | 15 | 远 | examples | · | 机场离市中心很远。 \| Jīchǎng lí shìzhōngxīn hěn yuǎn. \| The airport is far from downtown. | · | generated example sentence (uses only app vocab + allowed words) |
| 9fbdac11b958 | proposed | Places | 17 | 咖啡店 | examples | · | 这家咖啡店很安静。 \| Zhè jiā kāfēidiàn hěn ānjìng. \| This cafe is very quiet. | · | generated example sentence (uses only app vocab + allowed words) |
| 637ee9dd167e | proposed | Daily Life | 17 | 我没听见 | examples | · | 对不起，我没听见。 \| Duìbuqǐ, wǒ méi tīngjiàn. \| Sorry, I didn't hear. | · | generated example sentence (uses only app vocab + allowed words) |
| ba3889de64a0 | proposed | Descriptions | 16 | 辣 | examples | · | 火锅很辣。 \| Huǒguō hěn là. \| The hotpot is very spicy. | · | generated example sentence (uses only app vocab + allowed words) |
| 1dd5b692092a | proposed | Places | 52 | 餐厅 | examples | · | 这家餐厅的烤鸭很好吃。 \| zhè jiā cāntīng de kǎoyā hěn hǎochī. \| The roast duck at this restaurant is delicious. | · | generated example sentence (uses only app vocab + allowed words) |
| 62e710d57a72 | proposed | Transition Words | 63 | 结果 | type | phrase | conjunction | low | In the sense "as a result", 结果 works as a single-word clause connector (conjunction), not a phrase. |
| a8b5225f665a | proposed | Transition Words | 63 | 结果 | examples | · | 我没带雨伞,结果衣服都湿透了。 \| Wǒ méi dài yǔsǎn, jiéguǒ yīfu dōu shītòu le. \| I didn't bring an umbrella, and as a result my clothes got soaked. | · | generated example sentence (uses only app vocab + allowed words) |
| db282601324a | proposed | Places | 20 | 俱乐部 | examples | · | 我是这个俱乐部的会员。 \| Wǒ shì zhège jùlèbù de huìyuán. \| I'm a member of this club. | · | generated example sentence (uses only app vocab + allowed words) |
| 607d504f3d2f | proposed | Activities | 40 | 旅游 | examples | · | 我想去国外旅游。 \| wǒ xiǎng qù guówài lǚyóu. \| I want to travel abroad. | · | generated example sentence (uses only app vocab + allowed words) |
| e149d106caa5 | proposed | Descriptions | 29 | 深红色 | examples | · | 她买了一件深红色的衣服。 \| tā mǎi le yí jiàn shēn hóngsè de yīfu. \| She bought a dark red top. | · | generated example sentence (uses only app vocab + allowed words) |
| f5eb3cfcabf5 | proposed | Familiar People | 16 | 分手 | type | verb | VOV | medium | 分手 is a separable verb-object compound (e.g. 分了手), like 见面, which is already typed VOV. |
| c495c136b1ad | proposed | Familiar People | 16 | 分手 | examples | · | 他们分手了。 \| tāmen fēnshǒu le. \| They broke up. | · | generated example sentence (uses only app vocab + allowed words) |
| 39f98901d51f | proposed | Transition Words | 27 | 原本 | examples | · | 我原本想去，可是下雨了。 \| Wǒ yuánběn xiǎng qù, kěshì xiàyǔ le. \| I originally wanted to go, but it rained. | · | generated example sentence (uses only app vocab + allowed words) |
| a2ab0d1ccfd3 | proposed | Body | 48 | 发烧 | examples | · | 我发烧了，今天不能上班。 \| Wǒ fāshāo le, jīntiān bù néng shàngbān. \| I have a fever, so I can't go to work today. | · | generated example sentence (uses only app vocab + allowed words) |
| f1c2d3e06596 | proposed | Transition Words | 11 | 最后 | examples | · | 最后，我们去了酒吧。 \| zuìhòu, wǒmen qù le jiǔbā. \| In the end, we went to a bar. | · | generated example sentence (uses only app vocab + allowed words) |
| 3a2fc5b221b0 | proposed | Directions | 25 | 里面 | examples | · | 钥匙在包里面。 \| Yàoshi zài bāo lǐmiàn. \| The keys are inside the bag. | · | generated example sentence (uses only app vocab + allowed words) |
| e3f7ccf1a029 | proposed | Descriptions | 38 | 亮黄色 | examples | · | 那辆亮黄色的车太贵了。 \| nà liàng liàng huángsè de chē tài guì le. \| That neon yellow car is too expensive. | · | generated example sentence (uses only app vocab + allowed words) |
| f24014380c2f | proposed | Activities | 42 | 看电影 | examples | · | 我们晚上去看电影吧。 \| wǒmen wǎnshang qù kàn diànyǐng ba. \| Let's go see a movie tonight. | · | generated example sentence (uses only app vocab + allowed words) |
| 3ec5f6151362 | proposed | Activities | 4 | 徒步 | examples | · | 我们周末去徒步吧。 \| Wǒmen zhōumò qù túbù ba. \| Let's go hiking this weekend. | · | generated example sentence (uses only app vocab + allowed words) |
| 0ca4736fc136 | proposed | Professional | 24 | 工程师 | examples | · | 我哥哥是工程师。 \| Wǒ gēge shì gōngchéngshī. \| My older brother is an engineer. | · | generated example sentence (uses only app vocab + allowed words) |
| 08350b2e47a9 | proposed | Familiar People | 11 | 亲戚 | examples | · | 我的亲戚都住在乡下。 \| Wǒ de qīnqi dōu zhù zài xiāngxia. \| My relatives all live in the countryside. | · | generated example sentence (uses only app vocab + allowed words) |
| 32cb85e2e9b9 | proposed | Transition Words | 29 | 今天 | examples | · | 今天天气很好。 \| Jīntiān tiānqì hěn hǎo. \| The weather is nice today. | · | generated example sentence (uses only app vocab + allowed words) |
| e178413edddf | proposed | Activities | 58 | 出去玩 | examples | · | 明天我们出去玩吧。 \| Míngtiān wǒmen chūqù wán ba. \| Let's go out tomorrow. | · | generated example sentence (uses only app vocab + allowed words) |
| 4f5aa999f87a | proposed | Places | 54 | 店 | examples | · | 这家店的奶茶很甜。 \| zhè jiā diàn de nǎichá hěn tián. \| The milk tea at this shop is very sweet. | · | generated example sentence (uses only app vocab + allowed words) |
| d76dfb3df107 | proposed | Places | 49 | 药店 | examples | · | 药店在医院旁边。 \| yàodiàn zài yīyuàn pángbiān. \| The pharmacy is next to the hospital. | · | generated example sentence (uses only app vocab + allowed words) |
| 1c7814bc4cb0 | proposed | Places | 25 | 朋友家 | examples | · | 我今天晚上在朋友家吃饭。 \| Wǒ jīntiān wǎnshang zài péngyou jiā chīfàn. \| I'm eating at a friend's house tonight. | · | generated example sentence (uses only app vocab + allowed words) |
| 2df6659dd7a1 | proposed | Activities | 57 | 聚会 | examples | · | 周末我们在朋友家聚会。 \| Zhōumò wǒmen zài péngyou jiā jùhuì. \| We're having a get-together at a friend's place this weekend. | · | generated example sentence (uses only app vocab + allowed words) |
| 26a40d9a917b | proposed | Directions | 26 | 左 | examples | · | 我们往左还是往右？ \| Wǒmen wǎng zuǒ háishì wǎng yòu? \| Do we go left or right? | · | generated example sentence (uses only app vocab + allowed words) |
| 0833a93f8d20 | proposed | Daily Life | 39 | 学生 | examples | · | 他们都是学生。 \| tāmen dōu shì xuésheng. \| They are all students. | · | generated example sentence (uses only app vocab + allowed words) |
| dbba589e40ba | proposed | Daily Life | 30 | 早上 | examples | · | 我早上七点起床。 \| Wǒ zǎoshang qī diǎn qǐchuáng. \| I get up at seven in the morning. | · | generated example sentence (uses only app vocab + allowed words) |
| 25dd0a6488bf | proposed | Daily Life | 74 | 报名 | examples | · | 我想报名参加这个活动。 \| Wǒ xiǎng bàomíng cānjiā zhège huódòng. \| I want to sign up for this activity. | · | generated example sentence (uses only app vocab + allowed words) |
| b2e8438b96f0 | proposed | Objects | 49 | 垃圾 | examples | · | 我去扔垃圾。 \| wǒ qù rēng lājī. \| I'm going to take out the trash. | · | generated example sentence (uses only app vocab + allowed words) |
| 6360fa93261f | proposed | Transition Words | 49 | 是这样的 | examples | · | 是这样的，我明天要加班。 \| Shì zhèyàng de, wǒ míngtiān yào jiābān. \| So here's the thing: I have to work overtime tomorrow. | · | generated example sentence (uses only app vocab + allowed words) |
| c985aef4a322 | proposed | Transition Words | 6 | 偶尔 | examples | · | 我偶尔喝啤酒。 \| wǒ ǒu'ěr hē píjiǔ. \| I drink beer now and then. | · | generated example sentence (uses only app vocab + allowed words) |
| d761c1f7a04a | proposed | Places | 55 | 街 | examples | · | 这条街很热闹。 \| zhè tiáo jiē hěn rènao. \| This street is very lively. | · | generated example sentence (uses only app vocab + allowed words) |
| 52ee74641b78 | proposed | Daily Life | 89 | 随便你 | examples | · | 我们去哪儿？随便你。 \| wǒmen qù nǎr? suíbiàn nǐ. \| Where should we go? Up to you. | · | generated example sentence (uses only app vocab + allowed words) |
| bef5b7a2f4be | proposed | Transition Words | 69 | 连……都…… | type | phrase | pattern | medium | This is a grammar pattern with …… placeholders, so "pattern" is the fitting type. |
| a80f1654f595 | proposed | Transition Words | 69 | 连……都…… | examples | · | 这个很简单,连孩子都知道。 \| Zhège hěn jiǎndān, lián háizi dōu zhīdào. \| This is simple; even kids know it. | · | generated example sentence (uses only app vocab + allowed words) |
| c1b0612cc704 | proposed | Descriptions | 8 | 忙 | examples | · | 我今天很忙。 \| Wǒ jīntiān hěn máng. \| I'm busy today. | · | generated example sentence (uses only app vocab + allowed words) |
| 1a2ff097252d | proposed | Transition Words | 52 | 好像 | examples | · | 外面好像下雨了。 \| Wàimiàn hǎoxiàng xiàyǔ le. \| It seems like it's raining outside. | · | generated example sentence (uses only app vocab + allowed words) |
| e4a9cabaad3e | proposed | Transition Words | 21 | 上一次 | examples | · | 上一次我们去了动物园。 \| Shàng yí cì wǒmen qù le dòngwùyuán. \| Last time we went to the zoo. | · | generated example sentence (uses only app vocab + allowed words) |
| d229356a5fe4 | proposed | Body | 35 | 睡觉 | type | adjective | VOV | high | 睡觉 is a verb-object compound (睡 + 觉), as the card's own notes say; it is not an adjective. |
| 94b00a4b3b76 | proposed | Body | 35 | 睡觉 | examples | · | 我很困，想去睡觉。 \| Wǒ hěn kùn, xiǎng qù shuìjiào. \| I'm very sleepy and want to go to sleep. | · | generated example sentence (uses only app vocab + allowed words) |
| fb8125e0224b | proposed | Transition Words | 25 | 昨天 | examples | · | 昨天我很忙。 \| Zuótiān wǒ hěn máng. \| I was very busy yesterday. | · | generated example sentence (uses only app vocab + allowed words) |
| 32c736d3c114 | proposed | Activities | 49 | 弹 | examples | · | 你会弹什么？ \| nǐ huì tán shénme? \| What instrument can you play? | · | generated example sentence (uses only app vocab + allowed words) |
| 3de49d4601ec | proposed | Body | 33 | 心情好 | examples | · | 我今天心情好，想去公园散步。 \| Wǒ jīntiān xīnqíng hǎo, xiǎng qù gōngyuán sànbù. \| I'm in a good mood today and want to go for a walk in the park. | · | generated example sentence (uses only app vocab + allowed words) |
| 49196084cd69 | proposed | Places | 56 | 脱衣舞俱乐部 | examples | · | 那里有一家脱衣舞俱乐部。 \| Nàlǐ yǒu yì jiā tuōyīwǔ jùlèbù. \| There's a strip club over there. | · | generated example sentence (uses only app vocab + allowed words) |
| eadc8ee1c076 | proposed | Descriptions | 86 | 复杂 | examples | · | 这个项目很复杂。 \| zhège xiàngmù hěn fùzá. \| This project is complicated. | · | generated example sentence (uses only app vocab + allowed words) |
| 727514b95a3a | proposed | Descriptions | 21 | 黑色 | examples | · | 我有一个黑色的包。 \| Wǒ yǒu yí ge hēisè de bāo. \| I have a black bag. | · | generated example sentence (uses only app vocab + allowed words) |
| ce7290696277 | proposed | Transition Words | 72 | 由于 | examples | · | 由于下雨,我们没去公园。 \| Yóuyú xiàyǔ, wǒmen méi qù gōngyuán. \| Because of the rain, we didn't go to the park. | · | generated example sentence (uses only app vocab + allowed words) |
| 31d04b39f1af | proposed | Places | 35 | 岛 | examples | · | 这个岛很漂亮。 \| Zhège dǎo hěn piàoliang. \| This island is beautiful. | · | generated example sentence (uses only app vocab + allowed words) |
| d25938513b2f | proposed | Objects | 41 | 鞋 | examples | · | 这双鞋很舒服。 \| zhè shuāng xié hěn shūfu. \| These shoes are very comfortable. | · | generated example sentence (uses only app vocab + allowed words) |
| dd864dc75cc3 | proposed | Daily Life | 23 | 没关系 | examples | · | 对不起，我迟到了。没关系。 \| Duìbuqǐ, wǒ chídào le. Méi guānxi. \| Sorry I'm late. No worries. | · | generated example sentence (uses only app vocab + allowed words) |
| 70eda69caea8 | proposed | Descriptions | 50 | 小 | examples | · | 我的公寓太小了。 \| Wǒ de gōngyù tài xiǎo le. \| My apartment is too small. | · | generated example sentence (uses only app vocab + allowed words) |
| f43c70e6631e | proposed | Transition Words | 34 | 可是 | examples | · | 我很累，可是我还要工作。 \| Wǒ hěn lèi, kěshì wǒ hái yào gōngzuò. \| I'm tired, but I still have to work. | · | generated example sentence (uses only app vocab + allowed words) |
| 20c85dd162b7 | proposed | Descriptions | 83 | 免费 | examples | · | 这里的水是免费的。 \| Zhèlǐ de shuǐ shì miǎnfèi de. \| The water here is free. | · | generated example sentence (uses only app vocab + allowed words) |
| a65d2b615f54 | proposed | Directions | 51 | 长路口 | measure_word | · | 个 (gè) | medium | Noun card with no measure word. 路口 takes 个. |
| 301d5f3d000a | proposed | Directions | 51 | 长路口 | examples | · | 前面是一个长路口。 \| Qiánmiàn shì yí ge cháng lùkǒu. \| Up ahead is a long block. | · | generated example sentence (uses only app vocab + allowed words) |
| dde8c240374a | proposed | Transition Words | 71 | 同时 | examples | · | 我们同时到了机场。 \| Wǒmen tóngshí dào le jīchǎng. \| We arrived at the airport at the same time. | · | generated example sentence (uses only app vocab + allowed words) |
| 3c06f1703135 | proposed | Objects | 33 | 裤子 | examples | · | 这条裤子太长了。 \| zhè tiáo kùzi tài cháng le. \| These pants are too long. | · | generated example sentence (uses only app vocab + allowed words) |
| d883f60711cc | proposed | Transition Words | 13 | 突然 | examples | · | 突然下雨了。 \| tūrán xiàyǔ le. \| Suddenly it started raining. | · | generated example sentence (uses only app vocab + allowed words) |
| 1810ccea81b0 | proposed | Transition Words | 7 | 很少 | examples | · | 我很少看电视。 \| wǒ hěn shǎo kàn diànshì. \| I rarely watch TV. | · | generated example sentence (uses only app vocab + allowed words) |
| 8f304f0078ad | proposed | Body | 4 | 肚子饱了 | examples | · | 谢谢，我肚子饱了。 \| xièxie, wǒ dùzi bǎo le. \| Thanks, I'm full. | · | generated example sentence (uses only app vocab + allowed words) |
| d5346aa1046e | proposed | Objects | 32 | 面条 | examples | · | 这碗面条很好吃。 \| zhè wǎn miàntiáo hěn hǎochī. \| This bowl of noodles is delicious. | · | generated example sentence (uses only app vocab + allowed words) |
| 58af4d49d7b9 | proposed | Body | 54 | 药 | examples | · | 这个药很苦。 \| Zhège yào hěn kǔ. \| This medicine is very bitter. | · | generated example sentence (uses only app vocab + allowed words) |
| 2c4beffbca12 | proposed | Familiar People | 27 | 妈妈 | examples | · | 我妈妈很忙。 \| wǒ māma hěn máng. \| My mom is very busy. | · | generated example sentence (uses only app vocab + allowed words) |
| a3db854edb6a | proposed | Objects | 24 | 水果茶 | examples | · | 我要一杯水果茶。 \| Wǒ yào yì bēi shuǐguǒ chá. \| I'd like a cup of fruit tea. | · | generated example sentence (uses only app vocab + allowed words) |
| 1e803ca0c8a4 | proposed | Objects | 48 | 火车 | examples | · | 我们坐火车去吧。 \| wǒmen zuò huǒchē qù ba. \| Let's go by train. | · | generated example sentence (uses only app vocab + allowed words) |
| 5d9f0372fc3d | proposed | Activities | 23 | 筹款 | examples | · | 他们在公园筹款。 \| Tāmen zài gōngyuán chóukuǎn. \| They're fundraising in the park. | · | generated example sentence (uses only app vocab + allowed words) |
| 5c5a8494e6d7 | proposed | Directions | 53 | 路中间 | examples | · | 我的车坏在路中间了。 \| Wǒ de chē huài zài lù zhōngjiān le. \| My car broke down in the middle of the road. | · | generated example sentence (uses only app vocab + allowed words) |
| 6c9346621aca | proposed | Professional | 38 | 截止日期 | examples | · | 这个项目的截止日期是明天。 \| zhège xiàngmù de jiézhǐ rìqī shì míngtiān. \| The deadline for this project is tomorrow. | · | generated example sentence (uses only app vocab + allowed words) |
| 943cbe405b0a | proposed | Places | 30 | 家 | examples | · | 我今天在家休息。 \| Wǒ jīntiān zài jiā xiūxi. \| I'm resting at home today. | · | generated example sentence (uses only app vocab + allowed words) |
| 12bf09e244c6 | proposed | Descriptions | 28 | 深绿色 | examples | · | 他的车是深绿色的。 \| tā de chē shì shēn lǜsè de. \| His car is dark green. | · | generated example sentence (uses only app vocab + allowed words) |
| ba5852451844 | proposed | Descriptions | 39 | 橙色 | examples | · | 我的钱包是橙色的。 \| wǒ de qiánbāo shì chéngsè de. \| My wallet is orange. | · | generated example sentence (uses only app vocab + allowed words) |
| 6a40e321e724 | proposed | Transition Words | 70 | 一……就…… | type | sequence | pattern | medium | This is a two-part grammar pattern with …… placeholders, so "pattern" fits better than "sequence". |
| c3c9062bf487 | proposed | Transition Words | 70 | 一……就…… | examples | · | 我一到家就睡觉了。 \| Wǒ yí dào jiā jiù shuìjiào le. \| I went to sleep as soon as I got home. | · | generated example sentence (uses only app vocab + allowed words) |
| e21eb22d9bbf | proposed | Daily Life | 63 | 知道 | examples | · | 你知道他在哪儿吗？ \| Nǐ zhīdào tā zài nǎr ma? \| Do you know where he is? | · | generated example sentence (uses only app vocab + allowed words) |
| e29ee2198a1a | proposed | Activities | 25 | 参加 | examples | · | 我明天要参加一个会议。 \| Wǒ míngtiān yào cānjiā yí ge huìyì. \| I have to attend a meeting tomorrow. | · | generated example sentence (uses only app vocab + allowed words) |
| be0ea0fa08a5 | proposed | Professional | 22 | 公司 | examples | · | 我的公司在市中心。 \| Wǒ de gōngsī zài shìzhōngxīn. \| My company is downtown. | · | generated example sentence (uses only app vocab + allowed words) |
| 21c2147d914b | proposed | Directions | 19 | 上楼 | examples | · | 我们坐电梯上楼吧。 \| Wǒmen zuò diàntī shànglóu ba. \| Let's take the elevator upstairs. | · | generated example sentence (uses only app vocab + allowed words) |
| b182a5b5e570 | proposed | Familiar People | 19 | 结婚 | type | verb | VOV | medium | 结婚 is a separable verb-object compound (e.g. 结了婚, 结过婚). |
| 9af0d320295f | proposed | Familiar People | 19 | 结婚 | examples | · | 我姐姐结婚了。 \| wǒ jiějie jiéhūn le. \| My older sister got married. | · | generated example sentence (uses only app vocab + allowed words) |
| 6e5f1563bb73 | proposed | Objects | 17 | 电脑 | examples | · | 我的电脑坏了。 \| Wǒ de diànnǎo huài le. \| My computer is broken. | · | generated example sentence (uses only app vocab + allowed words) |
| 8c8afbc046dc | proposed | Objects | 22 | 花 | measure_word | 个 (gè) | 朵 (duǒ) | medium | The standard measure word for a single flower (bloom) is 朵; 束 (shù) is used for a bouquet and 枝 (zhī) for a stem. 个 is uncommon here. |
| bd0aa3fe2609 | proposed | Objects | 22 | 花 | examples | · | 她的花很漂亮。 \| Tā de huā hěn piàoliang. \| Her flowers are very pretty. | · | generated example sentence (uses only app vocab + allowed words) |
| fe407551f00a | proposed | Transition Words | 51 | 应该吧 | examples | · | 他明天会去吗？应该吧。 \| Tā míngtiān huì qù ma? Yīnggāi ba. \| Will he go tomorrow? Probably. | · | generated example sentence (uses only app vocab + allowed words) |
| c037e6213d19 | proposed | Body | 2 | 针灸 | examples | · | 针灸疼吗？ \| zhēnjiǔ téng ma? \| Does acupuncture hurt? | · | generated example sentence (uses only app vocab + allowed words) |
| b0ce290cde3c | proposed | Descriptions | 25 | 棕色 | examples | · | 我的狗是棕色的。 \| wǒ de gǒu shì zōngsè de. \| My dog is brown. | · | generated example sentence (uses only app vocab + allowed words) |
| 04572196852b | proposed | Places | 51 | 邮局 | examples | · | 邮局离这儿远吗？ \| yóujú lí zhèr yuǎn ma? \| Is the post office far from here? | · | generated example sentence (uses only app vocab + allowed words) |
| 17ae0016794a | proposed | Daily Life | 10 | 课 | examples | · | 我下午有课。 \| wǒ xiàwǔ yǒu kè. \| I have class this afternoon. | · | generated example sentence (uses only app vocab + allowed words) |
| 27e862409ade | proposed | Familiar People | 40 | 闺蜜 | examples | · | 她是我的闺蜜。 \| Tā shì wǒ de guīmì. \| She's my best girlfriend. | · | generated example sentence (uses only app vocab + allowed words) |
| 8d4f0fd0b003 | proposed | Daily Life | 68 | 下雨 | examples | · | 明天会下雨吗？ \| Míngtiān huì xiàyǔ ma? \| Will it rain tomorrow? | · | generated example sentence (uses only app vocab + allowed words) |
| 39a887bfc7a8 | proposed | Places | 16 | 公交站 | examples | · | 我家旁边有一个公交站。 \| Wǒ jiā pángbiān yǒu yí ge gōngjiāozhàn. \| There's a bus stop next to my home. | · | generated example sentence (uses only app vocab + allowed words) |
| de4c343c3781 | proposed | Activities | 29 | 跳舞 | examples | · | 我们晚上去酒吧跳舞吧。 \| Wǒmen wǎnshang qù jiǔbā tiàowǔ ba. \| Let's go dancing at a bar tonight. | · | generated example sentence (uses only app vocab + allowed words) |
| c232c8efbdc2 | proposed | Body | 21 | 我生病了 | examples | · | 我生病了，今天不去上班。 \| Wǒ shēngbìng le, jīntiān bú qù shàngbān. \| I'm sick, so I'm not going to work today. | · | generated example sentence (uses only app vocab + allowed words) |
| 8ed7c022cfc3 | proposed | Transition Words | 48 | 我觉得 | examples | · | 我觉得这个火锅很好吃。 \| Wǒ juéde zhège huǒguō hěn hǎochī. \| I think this hotpot is delicious. | · | generated example sentence (uses only app vocab + allowed words) |
| 2495feb885da | proposed | Directions | 35 | 边 | examples | · | 我们去海边散步吧。 \| Wǒmen qù hǎibiān sànbù ba. \| Let's go for a walk by the sea. | · | generated example sentence (uses only app vocab + allowed words) |
| f037c1e28c48 | proposed | Descriptions | 48 | 最好 | examples | · | 他是我最好的朋友。 \| Tā shì wǒ zuì hǎo de péngyou. \| He is my best friend. | · | generated example sentence (uses only app vocab + allowed words) |
| a12498a0b92e | proposed | Activities | 55 | 付钱 | examples | · | 你付钱了吗？ \| nǐ fùqián le ma? \| Have you paid? | · | generated example sentence (uses only app vocab + allowed words) |
| f0d0746454e9 | proposed | Daily Life | 34 | 别人 | examples | · | 这是别人的钱包。 \| Zhè shì biérén de qiánbāo. \| This is someone else's wallet. | · | generated example sentence (uses only app vocab + allowed words) |
| 85feee4c12b9 | proposed | Directions | 22 | 怎么去 | examples | · | 你明天怎么去机场？ \| Nǐ míngtiān zěnme qù jīchǎng? \| How are you getting to the airport tomorrow? | · | generated example sentence (uses only app vocab + allowed words) |
| a1a4fdb8cfd5 | proposed | Food | 5 | 赚 | examples | · | 他们卖奶茶赚了钱。 \| tāmen mài nǎichá zhuàn le qián. \| They made money selling milk tea. | · | generated example sentence (uses only app vocab + allowed words) |
| ec1b6c95d2f6 | proposed | Familiar People | 17 | 婚姻 | examples | · | 婚姻很重要。 \| hūnyīn hěn zhòngyào. \| Marriage is important. | · | generated example sentence (uses only app vocab + allowed words) |
| c1ed27e63b56 | proposed | Activities | 46 | 健身 | examples | · | 他下班以后去健身房健身。 \| tā xiàbān yǐhòu qù jiànshēnfáng jiànshēn. \| After work he goes to the gym to work out. | · | generated example sentence (uses only app vocab + allowed words) |
| 99840aba3d36 | proposed | Descriptions | 37 | 亮粉色 | examples | · | 她的手机是亮粉色的，很可爱。 \| tā de shǒujī shì liàng fěnsè de, hěn kě'ài. \| Her phone is neon pink — so cute. | · | generated example sentence (uses only app vocab + allowed words) |
| f6cae6214e27 | proposed | Objects | 37 | 爆米花 | examples | · | 我想买一份爆米花。 \| wǒ xiǎng mǎi yí fèn bàomǐhuā. \| I want to buy a portion of popcorn. | · | generated example sentence (uses only app vocab + allowed words) |
| 5ccd77974f93 | proposed | Transition Words | 79 | 期待 | examples | · | 我很期待这次旅游。 \| wǒ hěn qīdài zhè cì lǚyóu. \| I'm really looking forward to this trip. | · | generated example sentence (uses only app vocab + allowed words) |
| 6cc76c3bee2f | proposed | Daily Life | 44 | 问 | examples | · | 你问老师吧。 \| nǐ wèn lǎoshī ba. \| Ask the teacher. | · | generated example sentence (uses only app vocab + allowed words) |
| 3aa9259ffda5 | proposed | Professional | 17 | 演员 | examples | · | 这部电影的演员很好看。 \| Zhè bù diànyǐng de yǎnyuán hěn hǎokàn. \| The actors in this movie are really good-looking. | · | generated example sentence (uses only app vocab + allowed words) |
| 6c30c06e9e67 | proposed | Professional | 33 | 辞职 | examples | · | 我的同事辞职了。 \| wǒ de tóngshì cízhí le. \| My coworker quit. | · | generated example sentence (uses only app vocab + allowed words) |
| ba63320f6bb7 | proposed | Transition Words | 62 | 反正 | type | phrase | adverb | medium | 反正 is a single-word adverb (anyway / in any case), not a phrase. |
| 09b7a81cd3a9 | proposed | Transition Words | 62 | 反正 | examples | · | 反正我明天有空。 \| Fǎnzhèng wǒ míngtiān yǒu kòng. \| Anyway, I'm free tomorrow. | · | generated example sentence (uses only app vocab + allowed words) |
| c8d6088392d0 | proposed | Activities | 9 | 谈话 | type | verb | VOV | low | 谈话 is a verb-object compound (谈 + 话) and can be separated (谈过话). |
| 73f7f9ec1616 | proposed | Activities | 9 | 谈话 | examples | · | 老板想跟你谈话。 \| Lǎobǎn xiǎng gēn nǐ tánhuà. \| The boss wants to have a talk with you. | · | generated example sentence (uses only app vocab + allowed words) |
| 09c05593b8ab | proposed | Activities | 35 | 做饭 | examples | · | 我老公很会做饭。 \| Wǒ lǎogōng hěn huì zuòfàn. \| My husband is a really good cook. | · | generated example sentence (uses only app vocab + allowed words) |
| bf1f0146ca4a | proposed | Objects | 51 | 电视节目 | examples | · | 这个电视节目很有意思。 \| Zhège diànshì jiémù hěn yǒu yìsi. \| This TV show is really interesting. | · | generated example sentence (uses only app vocab + allowed words) |
| def2c32d899d | proposed | Descriptions | 80 | 有意思 | examples | · | 这部电影很有意思。 \| Zhè bù diànyǐng hěn yǒu yìsi. \| This movie is really interesting. | · | generated example sentence (uses only app vocab + allowed words) |
| de2f0077ba00 | proposed | Daily Life | 13 | 不好意思 | examples | · | 不好意思，我迟到了。 \| bù hǎoyìsi, wǒ chídào le. \| Sorry, I'm late. | · | generated example sentence (uses only app vocab + allowed words) |
| 35a9ccc35981 | proposed | Activities | 36 | 吃饭 | examples | · | 我们去中餐馆吃饭吧。 \| Wǒmen qù zhōngcānguǎn chīfàn ba. \| Let's go eat at a Chinese restaurant. | · | generated example sentence (uses only app vocab + allowed words) |
| b315d3d900a6 | proposed | Body | 39 | 鼻子 | measure_word | · | 个 (gè) | high | 鼻子 takes the general measure word 个 (一个鼻子). |
| d09f4fc67e91 | proposed | Body | 39 | 鼻子 | examples | · | 他的鼻子很高。 \| Tā de bízi hěn gāo. \| He has a high nose bridge. | · | generated example sentence (uses only app vocab + allowed words) |
| 3429ccb6b770 | proposed | Objects | 11 | 猫 | examples | · | 我有一只猫。 \| Wǒ yǒu yì zhī māo. \| I have a cat. | · | generated example sentence (uses only app vocab + allowed words) |
| c82b8270cbe6 | proposed | Objects | 10 | 车 | examples | · | 我的车很新。 \| Wǒ de chē hěn xīn. \| My car is very new. | · | generated example sentence (uses only app vocab + allowed words) |
| 0f303e4d2a0c | proposed | Objects | 16 | 咖啡 | examples | · | 我要一杯咖啡。 \| Wǒ yào yì bēi kāfēi. \| I'd like a cup of coffee. | · | generated example sentence (uses only app vocab + allowed words) |
| 0c88cbdad8c6 | proposed | Activities | 14 | 点外卖 | examples | · | 今天晚上我们点外卖吧。 \| Jīntiān wǎnshang wǒmen diǎn wàimài ba. \| Let's order takeout tonight. | · | generated example sentence (uses only app vocab + allowed words) |
| 04d6f921d470 | proposed | Descriptions | 51 | 新 | examples | · | 我有一个新手机。 \| Wǒ yǒu yí ge xīn shǒujī. \| I have a new phone. | · | generated example sentence (uses only app vocab + allowed words) |
| 2e21d01f601b | proposed | Descriptions | 73 | 吵 | examples | · | 这个酒吧太吵了。 \| Zhège jiǔbā tài chǎo le. \| This bar is too noisy. | · | generated example sentence (uses only app vocab + allowed words) |
| efec5d10bc09 | proposed | Body | 34 | 累 | examples | · | 我今天加班了，很累。 \| Wǒ jīntiān jiābān le, hěn lèi. \| I worked overtime today, so I'm very tired. | · | generated example sentence (uses only app vocab + allowed words) |
| b1071a537660 | proposed | Places | 42 | 山 | examples | · | 那座山很高。 \| nà zuò shān hěn gāo. \| That mountain is very high. | · | generated example sentence (uses only app vocab + allowed words) |
| 6353da78a201 | proposed | Transition Words | 30 | 刚才 | examples | · | 他刚才给我打电话了。 \| Tā gāngcái gěi wǒ dǎ diànhuà le. \| He called me just now. | · | generated example sentence (uses only app vocab + allowed words) |
| 3372e523610e | proposed | Daily Life | 91 | 微信 | examples | · | 你有微信吗？ \| nǐ yǒu Wēixìn ma? \| Do you have WeChat? | · | generated example sentence (uses only app vocab + allowed words) |
| cba5ebe6e540 | proposed | Directions | 3 | 路口 | measure_word | · | 个 (gè) | high | Standard measure word for 路口 (两个路口). |
| 83a4ca9f24c6 | proposed | Directions | 3 | 路口 | english | (city) blocks | intersection (used to count blocks) | medium | 路口 literally means intersection/crossing; it is only used to count blocks in directions. The gloss alone is misleading. |
| 3cf765b978f2 | proposed | Directions | 3 | 路口 | examples | · | 直走两个路口就到了。 \| Zhí zǒu liǎng ge lùkǒu jiù dào le. \| Go straight two blocks and you're there. | · | generated example sentence (uses only app vocab + allowed words) |
| c24e32e67240 | proposed | Descriptions | 53 | 老 | examples | · | 我爷爷已经很老了。 \| Wǒ yéye yǐjīng hěn lǎo le. \| My grandpa is already very old. | · | generated example sentence (uses only app vocab + allowed words) |
| 932abc7b4db0 | proposed | Objects | 14 | 鸡肉 | examples | · | 鸡肉很好吃。 \| Jīròu hěn hǎochī. \| The chicken is delicious. | · | generated example sentence (uses only app vocab + allowed words) |
| 87d036d61680 | proposed | Descriptions | 49 | 大 | examples | · | 这个房子很大。 \| Zhège fángzi hěn dà. \| This house is really big. | · | generated example sentence (uses only app vocab + allowed words) |
| 44ea31e4084b | proposed | Transition Words | 74 | 本来 | english | a moment ago / originally | originally / at first | high | 本来 does not mean 'a moment ago'; that is 刚才. 本来 means originally, at first, or 'was going to'. |
| b39d03251fe9 | proposed | Transition Words | 74 | 本来 | type | time | adverb | low | 本来 works as an adverb before the verb (我本来想去…). |
| 09b188d29a25 | proposed | Transition Words | 74 | 本来 | examples | · | 我本来想去，可是我太累了。 \| wǒ běnlái xiǎng qù, kěshì wǒ tài lèi le. \| I was originally going to go, but I was too tired. | · | generated example sentence (uses only app vocab + allowed words) |
| 98a5e69fda5f | proposed | Descriptions | 19 | 湿 | examples | · | 我的头发湿了。 \| Wǒ de tóufa shī le. \| My hair is wet. | · | generated example sentence (uses only app vocab + allowed words) |
| 5fc721a93ea3 | proposed | Daily Life | 47 | 迟到 | examples | · | 他上班又迟到了。 \| tā shàngbān yòu chídào le. \| He was late for work again. | · | generated example sentence (uses only app vocab + allowed words) |
| 1641a3002aa0 | proposed | Places | 24 | 操场 | english | exercise field | sports ground / playground | low | 操场 is normally glossed as a (school) sports ground or playground; "exercise field" is not a natural English term. |
| 93e93e6ce054 | proposed | Places | 24 | 操场 | examples | · | 我们在操场跑步。 \| Wǒmen zài cāochǎng pǎobù. \| We run on the sports ground. | · | generated example sentence (uses only app vocab + allowed words) |
| 54ea9ac0c408 | proposed | Places | 21 | 国家 | examples | · | 你去过几个国家？ \| Nǐ qù guo jǐ ge guójiā? \| How many countries have you been to? | · | generated example sentence (uses only app vocab + allowed words) |
| 6bd6fdb7ced4 | proposed | Daily Life | 12 | 晚上 | examples | · | 我晚上很少出去玩。 \| wǒ wǎnshang hěn shǎo chūqù wán. \| I rarely go out in the evening. | · | generated example sentence (uses only app vocab + allowed words) |
| 5c48eaac37be | proposed | Transition Words | 35 | 如果 | examples | · | 如果明天下雨，我就不去了。 \| Rúguǒ míngtiān xiàyǔ, wǒ jiù bú qù le. \| If it rains tomorrow, I won't go. | · | generated example sentence (uses only app vocab + allowed words) |
| 31631c4d0677 | proposed | Objects | 8 | 自行车 | examples | · | 我的自行车坏了。 \| Wǒ de zìxíngchē huài le. \| My bike is broken. | · | generated example sentence (uses only app vocab + allowed words) |
| 338afb6cbe08 | proposed | Transition Words | 18 | 这次 | examples | · | 这次我请客。 \| Zhè cì wǒ qǐngkè. \| This time it's my treat. | · | generated example sentence (uses only app vocab + allowed words) |
| e1c1373ce642 | proposed | Descriptions | 33 | 浅 | examples | · | 这里的海很浅。 \| zhèlǐ de hǎi hěn qiǎn. \| The water here is shallow. | · | generated example sentence (uses only app vocab + allowed words) |
| d4c928132ee2 | proposed | Descriptions | 17 | 生气 | examples | · | 他对我生气了。 \| Tā duì wǒ shēngqì le. \| He got mad at me. | · | generated example sentence (uses only app vocab + allowed words) |
| 2fac4b3c4fe3 | proposed | Daily Life | 43 | 道歉 | examples | · | 你要跟她道歉。 \| nǐ yào gēn tā dàoqiàn. \| You need to apologize to her. | · | generated example sentence (uses only app vocab + allowed words) |
| dd4a1f7c6bc8 | proposed | Places | 40 | 商场 | examples | · | 周末我们去商场逛街吧。 \| zhōumò wǒmen qù shāngchǎng guàngjiē ba. \| Let's go shopping at the mall this weekend. | · | generated example sentence (uses only app vocab + allowed words) |
| 2c8470f8aaba | proposed | Objects | 15 | 衣服 | examples | · | 这件衣服很漂亮。 \| Zhè jiàn yīfu hěn piàoliang. \| This piece of clothing is very pretty. | · | generated example sentence (uses only app vocab + allowed words) |
| f6a1df381b3f | proposed | Familiar People | 29 | 父母 | examples | · | 我父母住在老家。 \| wǒ fùmǔ zhù zài lǎojiā. \| My parents live in my hometown. | · | generated example sentence (uses only app vocab + allowed words) |
| 9c283533e680 | proposed | Places | 14 | 建筑 | examples | · | 这座建筑很漂亮。 \| Zhè zuò jiànzhù hěn piàoliang. \| This building is beautiful. | · | generated example sentence (uses only app vocab + allowed words) |
| 2fca9d06ad6d | proposed | Directions | 48 | 楼上 | examples | · | 我的卧室在楼上。 \| Wǒ de wòshì zài lóushàng. \| My bedroom is upstairs. | · | generated example sentence (uses only app vocab + allowed words) |
| 6282999be13b | proposed | Daily Life | 42 | 回答 | examples | · | 他没回答我。 \| tā méi huídá wǒ. \| He didn't answer me. | · | generated example sentence (uses only app vocab + allowed words) |
| 6dc8dc32d89d | proposed | Transition Words | 12 | 以前 | examples | · | 我睡觉以前刷牙。 \| wǒ shuìjiào yǐqián shuā yá. \| I brush my teeth before going to bed. | · | generated example sentence (uses only app vocab + allowed words) |
| 109c4fd9ac1f | proposed | Body | 22 | 肚子 | examples | · | 我的肚子有点儿疼。 \| Wǒ de dùzi yǒudiǎnr téng. \| My stomach hurts a bit. | · | generated example sentence (uses only app vocab + allowed words) |
| 3bb15313618f | proposed | Professional | 9 | 同事 | examples | · | 我的同事都很好。 \| Wǒ de tóngshì dōu hěn hǎo. \| My coworkers are all very nice. | · | generated example sentence (uses only app vocab + allowed words) |
| 616d8b32e082 | proposed | Places | 43 | 电影院 | examples | · | 我们去电影院看电影吧。 \| wǒmen qù diànyǐngyuàn kàn diànyǐng ba. \| Let's go to the movie theater to watch a movie. | · | generated example sentence (uses only app vocab + allowed words) |
| 191bc92103e7 | proposed | Daily Life | 62 | 赶 | examples | · | 我们要赶火车。 \| Wǒmen yào gǎn huǒchē. \| We have to hurry to catch the train. | · | generated example sentence (uses only app vocab + allowed words) |
| 3c51cd544f72 | proposed | Verbs | 2 | 脱 | examples | · | 太热了，我脱了一件衣服。 \| Tài rè le, wǒ tuō le yí jiàn yīfu. \| It was too hot, so I took off a layer. | · | generated example sentence (uses only app vocab + allowed words) |
| 64d402ca1515 | proposed | Transition Words | 57 | 等一下 | english | in a bit / later | wait a moment / in a bit | medium | In Mainland usage, 等一下 most commonly means "wait a moment". The "in a bit / later" sense is secondary, so the gloss as written leaves out the primary meaning. |
| 53ce27781f2a | proposed | Transition Words | 57 | 等一下 | examples | · | 等一下我给你打电话。 \| Děng yíxià wǒ gěi nǐ dǎ diànhuà. \| I'll call you in a bit. | · | generated example sentence (uses only app vocab + allowed words) |
| db9f4e33effc | proposed | Body | 61 | 渴 | examples | · | 我很渴。 \| Wǒ hěn kě. \| I'm very thirsty. | · | generated example sentence (uses only app vocab + allowed words) |
| 69dae10f718c | proposed | Places | 5 | 公寓楼 | examples | · | 我住在那栋公寓楼。 \| Wǒ zhù zài nà dòng gōngyù lóu. \| I live in that apartment building. | · | generated example sentence (uses only app vocab + allowed words) |
| 9531368d1620 | proposed | Descriptions | 64 | 帅 | examples | · | 她的男朋友很帅。 \| Tā de nán péngyou hěn shuài. \| Her boyfriend is really handsome. | · | generated example sentence (uses only app vocab + allowed words) |
| 2ff79685f457 | proposed | Transition Words | 60 | 或者 | examples | · | 我们可以喝茶或者咖啡。 \| Wǒmen kěyǐ hē chá huòzhě kāfēi. \| We can have tea or coffee. | · | generated example sentence (uses only app vocab + allowed words) |
| 9ec03decabf0 | proposed | Objects | 19 | 饺子 | examples | · | 我要一盘饺子。 \| Wǒ yào yì pán jiǎozi. \| I'd like a plate of dumplings. | · | generated example sentence (uses only app vocab + allowed words) |
| 26d801baba3f | proposed | Transition Words | 15 | 终于 | examples | · | 我终于到家了。 \| Wǒ zhōngyú dào jiā le. \| I finally got home. | · | generated example sentence (uses only app vocab + allowed words) |
| ba0caac30f86 | proposed | Transition Words | 47 | 对我来说 | examples | · | 对我来说，开车很难。 \| Duì wǒ lái shuō, kāichē hěn nán. \| For me, driving is hard. | · | generated example sentence (uses only app vocab + allowed words) |
| 4dd5634697d5 | proposed | Daily Life | 36 | 改天 | examples | · | 我今天很忙，我们改天去吧。 \| wǒ jīntiān hěn máng, wǒmen gǎitiān qù ba. \| I'm busy today, let's go some other day. | · | generated example sentence (uses only app vocab + allowed words) |
| 81b89bda0d92 | proposed | Directions | 49 | 西 | examples | · | 公园在学校的西边。 \| Gōngyuán zài xuéxiào de xī biān. \| The park is on the west side of the school. | · | generated example sentence (uses only app vocab + allowed words) |
| a1eebc9ef7b9 | proposed | Daily Life | 46 | 有空 | examples | · | 你明天有空吗？ \| nǐ míngtiān yǒu kòng ma? \| Are you free tomorrow? | · | generated example sentence (uses only app vocab + allowed words) |
| ee66e3625c47 | proposed | Body | 51 | 头疼 | english | headache | to have a headache / headache | low | The type is adjective, and 头疼 is used predicatively (我头疼). A noun-only gloss doesn't match how the word works. |
| b9e3a36f1a69 | proposed | Body | 51 | 头疼 | examples | · | 我今天头疼，不想去上班。 \| Wǒ jīntiān tóuténg, bù xiǎng qù shàngbān. \| I have a headache today and don't want to go to work. | · | generated example sentence (uses only app vocab + allowed words) |
| 465b7f05e7ea | proposed | Daily Life | 82 | 请客 | examples | · | 今天我请客。 \| jīntiān wǒ qǐngkè. \| Today it's my treat. | · | generated example sentence (uses only app vocab + allowed words) |
| c8df656021eb | proposed | Places | 11 | 海滩 | examples | · | 这个海滩很漂亮。 \| Zhège hǎitān hěn piàoliang. \| This beach is beautiful. | · | generated example sentence (uses only app vocab + allowed words) |
| 6a15d3d7bb46 | proposed | Descriptions | 24 | 亮 | examples | · | 外面很亮。 \| Wàimiàn hěn liàng. \| It's bright outside. | · | generated example sentence (uses only app vocab + allowed words) |
| 1c16ec39520e | proposed | Familiar People | 32 | 姐姐 | examples | · | 我姐姐在医院工作。 \| wǒ jiějie zài yīyuàn gōngzuò. \| My older sister works at a hospital. | · | generated example sentence (uses only app vocab + allowed words) |
| 5ac4d6ab21a0 | proposed | Descriptions | 34 | 淡 | examples | · | 这个汤有点儿淡。 \| zhège tāng yǒudiǎnr dàn. \| This soup is a bit bland. | · | generated example sentence (uses only app vocab + allowed words) |
| 0be4817caeab | proposed | Objects | 40 | 季票 | examples | · | 季票多少钱？ \| jìpiào duōshao qián? \| How much is the season pass? | · | generated example sentence (uses only app vocab + allowed words) |
| 0352727be3ef | proposed | Daily Life | 51 | 换 | examples | · | 我要换衣服。 \| wǒ yào huàn yīfu. \| I need to change clothes. | · | generated example sentence (uses only app vocab + allowed words) |
| 69d24882c964 | proposed | Body | 36 | 困 | examples | · | 我昨天晚上加班，现在很困。 \| Wǒ zuótiān wǎnshang jiābān, xiànzài hěn kùn. \| I worked overtime last night, so I'm really sleepy now. | · | generated example sentence (uses only app vocab + allowed words) |
| e792dfdc07fb | proposed | Transition Words | 33 | 但是 | examples | · | 这个很贵，但是很好吃。 \| Zhège hěn guì, dànshì hěn hǎochī. \| This is expensive, but it's delicious. | · | generated example sentence (uses only app vocab + allowed words) |
| 3222acf5ed07 | proposed | Descriptions | 32 | 绿色 | examples | · | 我的自行车是绿色的。 \| wǒ de zìxíngchē shì lǜsè de. \| My bike is green. | · | generated example sentence (uses only app vocab + allowed words) |
| 6c1b511b0745 | proposed | Objects | 39 | 烤鸭 | examples | · | 烤鸭很好吃。 \| kǎoyā hěn hǎochī. \| Roast duck is delicious. | · | generated example sentence (uses only app vocab + allowed words) |
| 26aa4e5a0e34 | proposed | Daily Life | 96 | 辛苦了 | examples | · | 你今天加班了，辛苦了！ \| nǐ jīntiān jiābān le, xīnkǔ le! \| You worked overtime today. Thanks for all your hard work! | · | generated example sentence (uses only app vocab + allowed words) |
| 0fe0a46cdb15 | proposed | Objects | 35 | 机票 | examples | · | 机票太贵了。 \| jīpiào tài guì le. \| The plane ticket is too expensive. | · | generated example sentence (uses only app vocab + allowed words) |
| 712efe6a6c2a | proposed | Transition Words | 32 | 因为 | examples | · | 因为下雨，所以我不去了。 \| Yīnwèi xiàyǔ, suǒyǐ wǒ bú qù le. \| Because it's raining, I'm not going anymore. | · | generated example sentence (uses only app vocab + allowed words) |
| 87596c4b1c73 | proposed | Places | 47 | 办公室 | examples | · | 老板在办公室。 \| lǎobǎn zài bàngōngshì. \| The boss is in the office. | · | generated example sentence (uses only app vocab + allowed words) |
| 9b055f7e9ac7 | proposed | Daily Life | 40 | 谢谢 | examples | · | 谢谢你帮我。 \| xièxie nǐ bāng wǒ. \| Thank you for helping me. | · | generated example sentence (uses only app vocab + allowed words) |
| 5291331cb9fe | proposed | Familiar People | 35 | 孩子 | examples | · | 你有孩子吗? \| nǐ yǒu háizi ma? \| Do you have kids? | · | generated example sentence (uses only app vocab + allowed words) |
| 483afd54a314 | proposed | Body | 41 | 牙 | examples | · | 我的牙很疼。 \| Wǒ de yá hěn téng. \| My tooth really hurts. | · | generated example sentence (uses only app vocab + allowed words) |
| 43956b075c6c | proposed | Daily Life | 6 | 你有空吗 | examples | · | 你有空吗？咱们去逛街吧。 \| nǐ yǒu kòng ma? zánmen qù guàngjiē ba. \| Are you free? Let's go shopping. | · | generated example sentence (uses only app vocab + allowed words) |
| 2855f944a3a2 | proposed | Body | 23 | 背 | measure_word | · | 个 (gè) | low | Noun card with no measure word. 背 is rarely counted, but 个 is the default when it is. |
| 681aabee06c6 | proposed | Body | 23 | 背 | examples | · | 我的背很疼。 \| Wǒ de bèi hěn téng. \| My back really hurts. | · | generated example sentence (uses only app vocab + allowed words) |
| 4fde2bccf48f | proposed | Directions | 33 | 外面 | examples | · | 外面很冷。 \| Wàimiàn hěn lěng. \| It's cold outside. | · | generated example sentence (uses only app vocab + allowed words) |
| 09e07af3a4f4 | proposed | Daily Life | 72 | 遇到 / 遇见 | pinyin | yùdào/yùjiàn | yùdào / yùjiàn | medium | Alternatives should be separated by " / " to line up with the hanzi "遇到 / 遇见". |
| 984164653a77 | proposed | Daily Life | 72 | 遇到 / 遇见 | examples | · | 我昨天在超市遇到了我的老师。 \| Wǒ zuótiān zài chāoshì yùdào le wǒ de lǎoshī. \| I ran into my teacher at the supermarket yesterday. | · | generated example sentence (uses only app vocab + allowed words) |
| 892185711892 | proposed | Descriptions | 10 | 脏 | examples | · | 你的衣服很脏。 \| Nǐ de yīfu hěn zāng. \| Your clothes are dirty. | · | generated example sentence (uses only app vocab + allowed words) |
| 62b47a69ff90 | proposed | Body | 29 | 眼睛 | examples | · | 她的眼睛很漂亮。 \| Tā de yǎnjing hěn piàoliang. \| Her eyes are beautiful. | · | generated example sentence (uses only app vocab + allowed words) |
| 502e3a1b7171 | proposed | Descriptions | 41 | 粉色 | examples | · | 我女儿的床是粉色的。 \| wǒ nǚ'ér de chuáng shì fěnsè de. \| My daughter's bed is pink. | · | generated example sentence (uses only app vocab + allowed words) |
| d6204fbdf371 | proposed | Daily Life | 25 | 说好了 | examples | · | 说好了，明天我请客。 \| Shuō hǎo le, míngtiān wǒ qǐngkè. \| It's settled — tomorrow it's my treat. | · | generated example sentence (uses only app vocab + allowed words) |
| feae2732c337 | proposed | Objects | 7 | 啤酒 | examples | · | 我们喝了两瓶啤酒。 \| Wǒmen hē le liǎng píng píjiǔ. \| We drank two bottles of beer. | · | generated example sentence (uses only app vocab + allowed words) |
| f0675e935d7c | proposed | Places | 62 | 夜俱乐部 | measure_word | · | 家 (jiā) | high | Businesses and venues take 家. |
| 264b42ce8056 | proposed | Places | 62 | 夜俱乐部 | hanzi | 夜俱乐部 | 夜店 | medium | 夜俱乐部 is rare and sounds like a literal translation. The standard words are 夜店 (colloquial) or 夜总会 (more formal/old-fashioned). |
| 571e475046a7 | proposed | Places | 62 | 夜俱乐部 | pinyin | yè jùlèbù | yèdiàn | medium | This should match the suggested hanzi 夜店. |
| 80dc3c73ac22 | proposed | Places | 62 | 夜俱乐部 | examples | · | 他们晚上去夜俱乐部跳舞。 \| Tāmen wǎnshang qù yè jùlèbù tiàowǔ. \| They go dancing at a nightclub in the evening. | · | generated example sentence (uses only app vocab + allowed words) |
| 1ff19e42858f | proposed | Daily Life | 41 | 太夸张了 | pinyin | tài kuā zhāng le | tài kuāzhāng le | low | 夸张 is a single word and is normally written as one pinyin word. |
| ce9f6857d73f | proposed | Daily Life | 41 | 太夸张了 | examples | · | 一杯咖啡一百块？太夸张了！ \| yì bēi kāfēi yìbǎi kuài? tài kuāzhāng le! \| A hundred kuai for one coffee? That's ridiculous! | · | generated example sentence (uses only app vocab + allowed words) |
| b0e8f2e4c6d7 | proposed | Objects | 25 | 游戏 | examples | · | 这个游戏很好玩。 \| Zhège yóuxì hěn hǎowán. \| This game is really fun. | · | generated example sentence (uses only app vocab + allowed words) |
| 3a6fb79982fd | proposed | Daily Life | 57 | 起床 | examples | · | 我早上七点起床。 \| Wǒ zǎoshang qī diǎn qǐchuáng. \| I get up at seven in the morning. | · | generated example sentence (uses only app vocab + allowed words) |
| 5846d0a120f4 | proposed | Professional | 30 | 上班 | examples | · | 我坐地铁上班。 \| Wǒ zuò dìtiě shàngbān. \| I take the subway to work. | · | generated example sentence (uses only app vocab + allowed words) |
| 45b668dd9f27 | proposed | Places | 28 | 理发店 / 美发店 | pinyin | lǐfàdiàn/měifàdiàn | lǐfàdiàn / měifàdiàn | medium | Alternatives must be separated by " / " to line up with the hanzi field. |
| 7c46f802d6e9 | proposed | Places | 28 | 理发店 / 美发店 | examples | · | 这家理发店很便宜。 \| Zhè jiā lǐfàdiàn hěn piányi. \| This hair salon is very cheap. | · | generated example sentence (uses only app vocab + allowed words) |
| b142b82ee244 | proposed | Daily Life | 90 | 天气 | examples | · | 今天天气很好。 \| jīntiān tiānqì hěn hǎo. \| The weather is nice today. | · | generated example sentence (uses only app vocab + allowed words) |
| 24aa618e63ed | proposed | Familiar People | 25 | 老公 | examples | · | 我老公很帅。 \| wǒ lǎogōng hěn shuài. \| My husband is very handsome. | · | generated example sentence (uses only app vocab + allowed words) |
| 9c6cf23e1032 | proposed | Directions | 11 | 方 | examples | · | 这个地方很漂亮。 \| Zhège dìfang hěn piàoliang. \| This place is beautiful. | · | generated example sentence (uses only app vocab + allowed words) |
| 7d73d0b3f4b9 | proposed | Transition Words | 3 | 经常 | english | often (formal) | often | medium | 经常 is not formal; it is the most common everyday word for 'often' (the card's own note says so). The 'formal' label is misleading. |
| 7a4ad1623433 | proposed | Transition Words | 3 | 经常 | examples | · | 我经常去健身房。 \| wǒ jīngcháng qù jiànshēnfáng. \| I often go to the gym. | · | generated example sentence (uses only app vocab + allowed words) |
| 8c9032a46530 | proposed | Familiar People | 12 | 对象 | examples | · | 你有对象了吗? \| Nǐ yǒu duìxiàng le ma? \| Are you seeing anyone yet? | · | generated example sentence (uses only app vocab + allowed words) |
| 7f327545a527 | proposed | Familiar People | 33 | 妹妹 | examples | · | 我妹妹是学生。 \| wǒ mèimei shì xuésheng. \| My younger sister is a student. | · | generated example sentence (uses only app vocab + allowed words) |
| c48ca927d148 | proposed | Transition Words | 54 | 一点儿 | examples | · | 可以便宜一点儿吗? \| Kěyǐ piányi yìdiǎnr ma? \| Can it be a little cheaper? | · | generated example sentence (uses only app vocab + allowed words) |
| da754d5c6257 | proposed | Directions | 52 | 短路口 | measure_word | · | 个 (gè) | medium | Noun card with no measure word. 路口 takes 个. |
| 9202283b47cd | proposed | Directions | 52 | 短路口 | examples | · | 这是一个短路口。 \| Zhè shì yí ge duǎn lùkǒu. \| This is a short block. | · | generated example sentence (uses only app vocab + allowed words) |
| c403ad3b13fb | proposed | Descriptions | 45 | 白色 | examples | · | 我的猫是白色的。 \| Wǒ de māo shì báisè de. \| My cat is white. | · | generated example sentence (uses only app vocab + allowed words) |
| 8ff70a21c19b | proposed | Places | 61 | 在一个路口 | english | at the same block | at the same intersection | medium | 路口 means intersection/street corner rather than block; here 一个 has the colloquial sense of 'the same', so the phrase means 'at the same intersection'. |
| 59ccdff0aae2 | proposed | Places | 61 | 在一个路口 | examples | · | 银行和超市在一个路口。 \| Yínháng hé chāoshì zài yí ge lùkǒu. \| The bank and the grocery store are at the same intersection. | · | generated example sentence (uses only app vocab + allowed words) |
| 718bdb8685d2 | proposed | Familiar People | 37 | 爷爷 | examples | · | 我爷爷住在乡下。 \| Wǒ yéye zhù zài xiāngxia. \| My grandpa lives in the countryside. | · | generated example sentence (uses only app vocab + allowed words) |
| 4c0078d86fca | proposed | Objects | 50 | 电视 | examples | · | 我在家看电视。 \| Wǒ zài jiā kàn diànshì. \| I watch TV at home. | · | generated example sentence (uses only app vocab + allowed words) |
| d71eb513da0a | proposed | Activities | 17 | 学习 | examples | · | 我们在图书馆学习。 \| Wǒmen zài túshūguǎn xuéxí. \| We study at the library. | · | generated example sentence (uses only app vocab + allowed words) |
| cbb8e32fcc11 | proposed | Daily Life | 31 | 没事儿 | examples | · | 对不起！没事儿。 \| Duìbuqǐ! Méishìr. \| Sorry! It's nothing. | · | generated example sentence (uses only app vocab + allowed words) |
| 9ca718b1d086 | proposed | Body | 59 | 感觉 | examples | · | 我感觉很累。 \| Wǒ gǎnjué hěn lèi. \| I feel really tired. | · | generated example sentence (uses only app vocab + allowed words) |
| 0fe17112bafd | proposed | Objects | 13 | 椅子 | examples | · | 这把椅子很舒服。 \| Zhè bǎ yǐzi hěn shūfu. \| This chair is very comfortable. | · | generated example sentence (uses only app vocab + allowed words) |
| 8c800216fa66 | proposed | Professional | 36 | 简历 | examples | · | 这是我的简历。 \| zhè shì wǒ de jiǎnlì. \| This is my resume. | · | generated example sentence (uses only app vocab + allowed words) |
| 98912f2ad4c7 | proposed | Objects | 26 | 火锅 | examples | · | 火锅太辣了。 \| Huǒguō tài là le. \| The hotpot is too spicy. | · | generated example sentence (uses only app vocab + allowed words) |
| 60fe7d555b1a | proposed | Daily Life | 38 | 暴雨 | examples | · | 昨天下了一场暴雨。 \| zuótiān xià le yì chǎng bàoyǔ. \| There was a rainstorm yesterday. | · | generated example sentence (uses only app vocab + allowed words) |
| 0dd38d5c2666 | proposed | Descriptions | 56 | 好 | examples | · | 今天天气很好。 \| Jīntiān tiānqì hěn hǎo. \| The weather is nice today. | · | generated example sentence (uses only app vocab + allowed words) |
| 2fae3955388f | proposed | Activities | 27 | 租 | examples | · | 我想在市中心租一套公寓。 \| Wǒ xiǎng zài shìzhōngxīn zū yí tào gōngyù. \| I want to rent an apartment downtown. | · | generated example sentence (uses only app vocab + allowed words) |
| c4215bee08ab | proposed | Daily Life | 53 | 决定 | examples | · | 我决定去国外旅游。 \| wǒ juédìng qù guówài lǚyóu. \| I decided to travel abroad. | · | generated example sentence (uses only app vocab + allowed words) |
| 335364ca7aa4 | proposed | Descriptions | 14 | 比较 | examples | · | 这个餐厅比较贵。 \| Zhège cāntīng bǐjiào guì. \| This restaurant is relatively expensive. | · | generated example sentence (uses only app vocab + allowed words) |
| e3971eaff48c | proposed | Objects | 52 | 雨伞 | examples | · | 我的雨伞在哪儿？ \| Wǒ de yǔsǎn zài nǎr? \| Where is my umbrella? | · | generated example sentence (uses only app vocab + allowed words) |
| 2528cad7790b | proposed | Objects | 44 | 地铁 | measure_word | · | 趟 (tàng) | medium | Noun with no measure word. 趟 is commonly used for a subway run or trip (坐一趟地铁). 条 is used for subway lines and 列 for the train itself. |
| 3586e1051e11 | proposed | Places | 57 | 地铁 | measure_word | · | 趟 (tàng) | medium | Noun with no measure word. 趟 is commonly used for a subway run or trip (坐一趟地铁). 条 is used for subway lines and 列 for the train itself. |
| c1214b9b1ee8 | proposed | Objects | 44 | 地铁 | examples | · | 我坐地铁去上班。 \| wǒ zuò dìtiě qù shàngbān. \| I take the subway to work. | · | generated example sentence (uses only app vocab + allowed words) |
| 73d6327e9d89 | proposed | Familiar People | 26 | 老婆 | examples | · | 我老婆是老师。 \| wǒ lǎopo shì lǎoshī. \| My wife is a teacher. | · | generated example sentence (uses only app vocab + allowed words) |
| 4b88f76a5fc1 | proposed | Transition Words | 65 | 对了 | examples | · | 对了,你明天有空吗? \| Duìle, nǐ míngtiān yǒu kòng ma? \| By the way, are you free tomorrow? | · | generated example sentence (uses only app vocab + allowed words) |
| 802422879898 | proposed | Familiar People | 23 | 爱人 | english | lover | spouse (husband / wife) | medium | In Mainland Mandarin, which the app teaches, 爱人 primarily means spouse. The gloss 'lover' is misleading, even though the notes explain this. |
| dec98bff7f34 | proposed | Familiar People | 23 | 爱人 | examples | · | 我爱人是医生。 \| wǒ àirén shì yīshēng. \| My spouse is a doctor. | · | generated example sentence (uses only app vocab + allowed words) |
| ccc0e096b89c | proposed | Transition Words | 17 | 的时候 | examples | · | 我吃饭的时候不看手机。 \| Wǒ chīfàn de shíhou bú kàn shǒujī. \| I don't look at my phone when I'm eating. | · | generated example sentence (uses only app vocab + allowed words) |
| c16ed816c3cc | proposed | Descriptions | 63 | 可爱 | examples | · | 你的猫真可爱！ \| Nǐ de māo zhēn kě'ài! \| Your cat is so cute! | · | generated example sentence (uses only app vocab + allowed words) |
| 8728c8e70661 | proposed | Activities | 47 | 拍照 | examples | · | 这里可以拍照吗？ \| zhèlǐ kěyǐ pāizhào ma? \| Can I take photos here? | · | generated example sentence (uses only app vocab + allowed words) |
| af920abfc798 | proposed | Descriptions | 65 | 难 | examples | · | 这个游戏很难。 \| Zhège yóuxì hěn nán. \| This game is hard. | · | generated example sentence (uses only app vocab + allowed words) |
| 01d5faebad02 | proposed | Body | 10 | 痒 | examples | · | 我的背很痒。 \| wǒ de bèi hěn yǎng. \| My back is really itchy. | · | generated example sentence (uses only app vocab + allowed words) |
| 092ac93985b7 | proposed | Activities | 50 | 等 | examples | · | 我在地铁站等你。 \| wǒ zài dìtiězhàn děng nǐ. \| I'll wait for you at the subway station. | · | generated example sentence (uses only app vocab + allowed words) |
| 83c559d57bbf | proposed | Daily Life | 69 | 认识 | examples | · | 我认识他的女朋友。 \| Wǒ rènshi tā de nǚ péngyou. \| I know his girlfriend. | · | generated example sentence (uses only app vocab + allowed words) |
| 9f2f1446a136 | proposed | Objects | 53 | 蔬菜 | measure_word | · | 种 (zhǒng) | medium | 蔬菜 is usually counted by kind (一种蔬菜) or quantified with 些; 种 is the standard classifier. |
| a30e58a28464 | proposed | Objects | 53 | 蔬菜 | examples | · | 超市的蔬菜很新鲜。 \| Chāoshì de shūcài hěn xīnxian. \| The vegetables at the grocery store are very fresh. | · | generated example sentence (uses only app vocab + allowed words) |
| 5f4c69465b18 | proposed | Objects | 3 | 活动 | examples | · | 这个活动很有意思。 \| Zhège huódòng hěn yǒu yìsi. \| This activity is really interesting. | · | generated example sentence (uses only app vocab + allowed words) |
| 46cb83460566 | proposed | Objects | 42 | 配料 | english | side dishes / toppings | toppings / ingredients | medium | 配料 means added ingredients, toppings or seasonings (e.g. in milk tea or hotpot). A side dish is 配菜, as the card's own note says, so 'side dishes' is misleading. |
| 9d36fe408fdc | proposed | Objects | 42 | 配料 | examples | · | 奶茶的配料是免费的。 \| nǎichá de pèiliào shì miǎnfèi de. \| The milk tea toppings are free. | · | generated example sentence (uses only app vocab + allowed words) |
| f668300e885b | proposed | Daily Life | 11 | 晚饭 | examples | · | 今天的晚饭很好吃。 \| jīntiān de wǎnfàn hěn hǎochī. \| Tonight's dinner is delicious. | · | generated example sentence (uses only app vocab + allowed words) |
| 6dc99b550055 | proposed | Body | 58 | 个子 | examples | · | 他个子很高。 \| Tā gèzi hěn gāo. \| He is very tall. | · | generated example sentence (uses only app vocab + allowed words) |
| 73832d3a7a2f | proposed | Transition Words | 24 | 明天 | examples | · | 明天我要上班。 \| Míngtiān wǒ yào shàngbān. \| I have to go to work tomorrow. | · | generated example sentence (uses only app vocab + allowed words) |
| 1d38485c6460 | proposed | Daily Life | 45 | 可以 | examples | · | 我可以坐这儿吗？ \| wǒ kěyǐ zuò zhèr ma? \| Can I sit here? | · | generated example sentence (uses only app vocab + allowed words) |
| fef9082b076b | proposed | Transition Words | 9 | 首先 | examples | · | 首先，我们去超市，然后回家。 \| shǒuxiān, wǒmen qù chāoshì, ránhòu huíjiā. \| First we'll go to the supermarket, then go home. | · | generated example sentence (uses only app vocab + allowed words) |
| be7bb0b27e13 | proposed | Body | 46 | 膝盖 | examples | · | 我跑步以后膝盖很疼。 \| Wǒ pǎobù yǐhòu xīgài hěn téng. \| My knees hurt after I go running. | · | generated example sentence (uses only app vocab + allowed words) |
| 4133d6c69135 | proposed | Daily Life | 76 | 分 | examples | · | 咱们分这盘饺子吧。 \| Zánmen fēn zhè pán jiǎozi ba. \| Let's split this plate of dumplings. | · | generated example sentence (uses only app vocab + allowed words) |
| 9818cb9c6be1 | proposed | Daily Life | 77 | 开 | examples | · | 超市几点开？ \| Chāoshì jǐ diǎn kāi? \| What time does the supermarket open? | · | generated example sentence (uses only app vocab + allowed words) |
| 041525d41e9a | proposed | Professional | 16 | 性工作者 | examples | · | 她的朋友是性工作者。 \| Tā de péngyou shì xìng gōngzuòzhě. \| Her friend is a sex worker. | · | generated example sentence (uses only app vocab + allowed words) |
| 73e1cfcd34b1 | proposed | Body | 18 | 洗脸 | examples | · | 我刷牙，然后洗脸。 \| Wǒ shuā yá, ránhòu xǐliǎn. \| I brush my teeth, then wash my face. | · | generated example sentence (uses only app vocab + allowed words) |
| a06d8ef51f3f | proposed | Directions | 29 | 近 | examples | · | 我家离公园很近。 \| Wǒ jiā lí gōngyuán hěn jìn. \| My home is very close to the park. | · | generated example sentence (uses only app vocab + allowed words) |
| eaaeae30eb04 | proposed | Familiar People | 34 | 儿子 | examples | · | 他有两个儿子。 \| tā yǒu liǎng ge érzi. \| He has two sons. | · | generated example sentence (uses only app vocab + allowed words) |
| 53102543e3f2 | proposed | Body | 47 | 皮肤 | examples | · | 我的皮肤很痒。 \| Wǒ de pífū hěn yǎng. \| My skin is really itchy. | · | generated example sentence (uses only app vocab + allowed words) |
| 48f0d9fc44d9 | proposed | Transition Words | 4 | 常常 | english | often (informal) | often | medium | 常常 is not more informal than 经常; if anything it leans slightly literary. The 'informal' label is misleading. |
| ab0642b98e04 | proposed | Transition Words | 4 | 常常 | examples | · | 我常常在家做饭。 \| wǒ chángcháng zài jiā zuòfàn. \| I often cook at home. | · | generated example sentence (uses only app vocab + allowed words) |
| a835195e1069 | proposed | Places | 50 | 地方 | examples | · | 这个地方很漂亮。 \| zhège dìfang hěn piàoliang. \| This place is beautiful. | · | generated example sentence (uses only app vocab + allowed words) |
| 987914c13899 | proposed | Body | 8 | 手 | examples | · | 我的手很脏。 \| wǒ de shǒu hěn zāng. \| My hands are dirty. | · | generated example sentence (uses only app vocab + allowed words) |
| 010ab67019e9 | proposed | Familiar People | 43 | 暗恋 | type | VOV | verb | high | 暗恋 is adverb + verb (secretly + love), not a verb-object compound; it takes a direct object (我暗恋他). |
| 01e3fff01a3a | proposed | Familiar People | 43 | 暗恋 | examples | · | 我暗恋我的同学。 \| Wǒ ànliàn wǒ de tóngxué. \| I have a crush on my classmate. | · | generated example sentence (uses only app vocab + allowed words) |
| f6e0ae897e23 | proposed | Descriptions | 60 | 开心 | examples | · | 今天我很开心。 \| Jīntiān wǒ hěn kāixīn. \| I'm really happy today. | · | generated example sentence (uses only app vocab + allowed words) |
| 7c0a922b88c3 | proposed | Directions | 30 | 旁边 | examples | · | 药店在银行旁边。 \| Yàodiàn zài yínháng pángbiān. \| The pharmacy is next to the bank. | · | generated example sentence (uses only app vocab + allowed words) |
| cd5a2bae0e1c | proposed | Objects | 54 | 钱包 | examples | · | 我的钱包是黑色的。 \| Wǒ de qiánbāo shì hēisè de. \| My wallet is black. | · | generated example sentence (uses only app vocab + allowed words) |
| 43d859690a0e | proposed | Places | 58 | 地铁站 | examples | · | 地铁站离我家很近。 \| Dìtiězhàn lí wǒ jiā hěn jìn. \| The subway station is very close to my home. | · | generated example sentence (uses only app vocab + allowed words) |
| 5cd5cf487116 | proposed | Familiar People | 2 | 老板 | examples | · | 我的老板很忙。 \| Wǒ de lǎobǎn hěn máng. \| My boss is very busy. | · | generated example sentence (uses only app vocab + allowed words) |
| d15ea06bd622 | proposed | Transition Words | 55 | 我会 / 我要 / 我打算 | examples | · | 明天我会去银行。 \| Míngtiān wǒ huì qù yínháng. \| I'll go to the bank tomorrow. | · | generated example sentence (uses only app vocab + allowed words) |
| 402293035751 | proposed | Objects | 34 | 充电器 | examples | · | 你有充电器吗？ \| nǐ yǒu chōngdiànqì ma? \| Do you have a phone charger? | · | generated example sentence (uses only app vocab + allowed words) |
| f3d5e75a74a7 | proposed | Daily Life | 35 | 电话号码 | examples | · | 你的电话号码是多少？ \| nǐ de diànhuà hàomǎ shì duōshao? \| What's your phone number? | · | generated example sentence (uses only app vocab + allowed words) |
| 814a902b1349 | proposed | Objects | 47 | 票 | examples | · | 你买票了吗？ \| nǐ mǎi piào le ma? \| Did you buy a ticket? | · | generated example sentence (uses only app vocab + allowed words) |
| 0fb118568526 | proposed | Body | 45 | 手指 | examples | · | 她的手指很长。 \| Tā de shǒuzhǐ hěn cháng. \| She has long fingers. | · | generated example sentence (uses only app vocab + allowed words) |
| 7d3159edf5de | proposed | Directions | 5 | 地址 | measure_word | · | 个 (gè) | high | Standard measure word for 地址. |
| a75665ac6717 | proposed | Directions | 5 | 地址 | examples | · | 你家的地址是什么？ \| Nǐ jiā de dìzhǐ shì shénme? \| What's your home address? | · | generated example sentence (uses only app vocab + allowed words) |
| e704110789d3 | proposed | Familiar People | 36 | 奶奶 | examples | · | 我奶奶早上常常喝茶。 \| Wǒ nǎinai zǎoshang chángcháng hēchá. \| My grandma often drinks tea in the morning. | · | generated example sentence (uses only app vocab + allowed words) |
| 2d565fcc49a6 | proposed | Directions | 54 | 急转 | hanzi | 急转 | 急转弯 | medium | 急转 is mainly a verb ('to turn sharply'). The noun 'sharp turn' is normally 急转弯. |
| 800600c77b23 | proposed | Directions | 54 | 急转 | pinyin | jí zhuǎn | jízhuǎnwān | medium | This pinyin goes with the suggested hanzi 急转弯. |
| 439d4df05725 | proposed | Directions | 54 | 急转 | measure_word | · | 个 (gè) | low | Noun card with no measure word. A sharp turn is counted with 个. |
| 9c6d9fe354b7 | proposed | Directions | 54 | 急转 | examples | · | 前面有一个急转，你开车要慢一点儿。 \| Qiánmiàn yǒu yí ge jí zhuǎn, nǐ kāichē yào màn yìdiǎnr. \| There's a sharp turn ahead, so drive a bit slower. | · | generated example sentence (uses only app vocab + allowed words) |
| 2da51b271bed | proposed | Familiar People | 8 | 女朋友 | examples | · | 他的女朋友很漂亮。 \| Tā de nǚ péngyou hěn piàoliang. \| His girlfriend is very pretty. | · | generated example sentence (uses only app vocab + allowed words) |
| ea9ef6f16d85 | proposed | Daily Life | 55 | 找 | english | to find | to look for / to find | medium | 找 on its own mainly means 'to look for'. 'To find', meaning to succeed in finding, is usually 找到. |
| 6c81c88b4ce5 | proposed | Daily Life | 55 | 找 | examples | · | 我在找我的钥匙。 \| wǒ zài zhǎo wǒ de yàoshi. \| I'm looking for my keys. | · | generated example sentence (uses only app vocab + allowed words) |
| b80d0b3255e4 | proposed | Familiar People | 10 | 酷儿 | examples | · | 我的朋友是酷儿。 \| Wǒ de péngyou shì kù'ér. \| My friend is queer. | · | generated example sentence (uses only app vocab + allowed words) |
| 3c98fef75ca6 | proposed | Descriptions | 30 | 金色 | examples | · | 她的头发是金色的。 \| tā de tóufa shì jīnsè de. \| Her hair is blonde. | · | generated example sentence (uses only app vocab + allowed words) |
| 7a978f655de6 | proposed | Body | 37 | 脸 | measure_word | · | 张 (zhāng) | high | 张 is the standard measure word for faces (一张脸). |
| 1bb58a2f8880 | proposed | Body | 37 | 脸 | examples | · | 她的脸很小。 \| Tā de liǎn hěn xiǎo. \| She has a small face. | · | generated example sentence (uses only app vocab + allowed words) |
| 92bfc6ae58d4 | proposed | Places | 3 | 机场 | measure_word | 栋 (dòng) | 个 (gè) | medium | 栋 counts individual buildings; an airport is a whole facility and is counted with 个 (or 座), not 栋. |
| 3261e9e21d89 | proposed | Places | 3 | 机场 | examples | · | 我们坐地铁去机场。 \| Wǒmen zuò dìtiě qù jīchǎng. \| We take the subway to the airport. | · | generated example sentence (uses only app vocab + allowed words) |
| 9f5da15fcda1 | proposed | Daily Life | 61 | 帮 | examples | · | 你可以帮我吗？ \| Nǐ kěyǐ bāng wǒ ma? \| Can you help me? | · | generated example sentence (uses only app vocab + allowed words) |
| da8de1e39bc9 | proposed | Places | 32 | 医院 | examples | · | 我爸爸在医院工作。 \| Wǒ bàba zài yīyuàn gōngzuò. \| My dad works at a hospital. | · | generated example sentence (uses only app vocab + allowed words) |
| e99e736b50b0 | proposed | Transition Words | 45 | 比如 | examples | · | 我常常运动，比如跑步和游泳。 \| Wǒ chángcháng yùndòng, bǐrú pǎobù hé yóuyǒng. \| I often exercise, for example running and swimming. | · | generated example sentence (uses only app vocab + allowed words) |
| 9e156fe6aa2d | proposed | Daily Life | 59 | 去 | examples | · | 我们明天去公园吧。 \| Wǒmen míngtiān qù gōngyuán ba. \| Let's go to the park tomorrow. | · | generated example sentence (uses only app vocab + allowed words) |
| 8f1fa9f443cd | proposed | Daily Life | 85 | 用 | examples | · | 我可以用你的手机吗？ \| wǒ kěyǐ yòng nǐ de shǒujī ma? \| Can I use your phone? | · | generated example sentence (uses only app vocab + allowed words) |
| a950113fca90 | proposed | Directions | 38 | 到 | examples | · | 我们到机场了。 \| Wǒmen dào jīchǎng le. \| We've arrived at the airport. | · | generated example sentence (uses only app vocab + allowed words) |
| 8594515ee17a | proposed | Places | 39 | 客厅 | examples | · | 我们的客厅很大。 \| wǒmen de kètīng hěn dà. \| Our living room is very big. | · | generated example sentence (uses only app vocab + allowed words) |
| 4bb7fde9c291 | proposed | Transition Words | 14 | 就 | examples | · | 我现在就去。 \| Wǒ xiànzài jiù qù. \| I'll go right now. | · | generated example sentence (uses only app vocab + allowed words) |
| e1e7b74045d7 | proposed | Transition Words | 42 | 几次 / 多少次 | examples | · | 你去过那个博物馆几次？ \| Nǐ qù guo nàge bówùguǎn jǐ cì? \| How many times have you been to that museum? | · | generated example sentence (uses only app vocab + allowed words) |
| bfdc9bc341de | proposed | Descriptions | 42 | 紫色 | examples | · | 那件紫色的衣服很漂亮。 \| nà jiàn zǐsè de yīfu hěn piàoliang. \| That purple top is really pretty. | · | generated example sentence (uses only app vocab + allowed words) |
| c41cea7b267a | proposed | Descriptions | 68 | 慢 | examples | · | 这个电梯太慢了。 \| Zhège diàntī tài màn le. \| This elevator is too slow. | · | generated example sentence (uses only app vocab + allowed words) |
| 3736c6270df8 | proposed | Objects | 43 | 汤 | examples | · | 这碗汤太咸了。 \| zhè wǎn tāng tài xián le. \| This bowl of soup is too salty. | · | generated example sentence (uses only app vocab + allowed words) |
| cc31edf60e3c | proposed | Familiar People | 46 | 介绍 | type | VOV | verb | high | 介绍 is a regular transitive verb, not a verb-object compound. |
| 9da0fe4431e9 | proposed | Familiar People | 46 | 介绍 | examples | · | 我给你介绍一个朋友。 \| Wǒ gěi nǐ jièshào yí ge péngyou. \| Let me introduce a friend to you. | · | generated example sentence (uses only app vocab + allowed words) |
| dfcfa1a95947 | proposed | Transition Words | 68 | 要是……就…… | type | conjunction | pattern | medium | This is a two-part grammar pattern with …… placeholders, so "pattern" is the fitting type. |
| 07a07a62df4c | proposed | Transition Words | 68 | 要是……就…… | examples | · | 要是明天下雨,我们就不去了。 \| Yàoshi míngtiān xiàyǔ, wǒmen jiù bú qù le. \| If it rains tomorrow, we won't go. | · | generated example sentence (uses only app vocab + allowed words) |
| 3ae0409b73d9 | proposed | Transition Words | 76 | 当然 | type | phrase | adverb | low | 当然 is a single word that works as an adverb ('of course, naturally'). |
| 05ae99386f85 | proposed | Transition Words | 76 | 当然 | examples | · | 我当然记得你。 \| wǒ dāngrán jìde nǐ. \| Of course I remember you. | · | generated example sentence (uses only app vocab + allowed words) |
| bf0e738ebbc6 | proposed | Places | 44 | 博物馆 | examples | · | 这个博物馆很有意思。 \| zhège bówùguǎn hěn yǒu yìsi. \| This museum is very interesting. | · | generated example sentence (uses only app vocab + allowed words) |
| 150bb0cfbe38 | proposed | Activities | 26 | 脱口秀 | examples | · | 我们晚上去看脱口秀吧。 \| Wǒmen wǎnshang qù kàn tuōkǒuxiù ba. \| Let's go see a stand-up comedy show tonight. | · | generated example sentence (uses only app vocab + allowed words) |
| 27b5c0441b6f | proposed | Activities | 53 | 买 | examples | · | 我想买一双鞋。 \| wǒ xiǎng mǎi yì shuāng xié. \| I want to buy a pair of shoes. | · | generated example sentence (uses only app vocab + allowed words) |
| 09fb46df1841 | proposed | Professional | 28 | 客户 | examples | · | 经理今天跟客户开会。 \| Jīnglǐ jīntiān gēn kèhù kāihuì. \| The manager has a meeting with a client today. | · | generated example sentence (uses only app vocab + allowed words) |
| da565435b6fb | proposed | Daily Life | 80 | 扔 | examples | · | 我去扔垃圾。 \| wǒ qù rēng lājī. \| I'll go take out the trash. | · | generated example sentence (uses only app vocab + allowed words) |
| a127381ca573 | proposed | Places | 46 | 海 | examples | · | 那里的海很漂亮。 \| nàlǐ de hǎi hěn piàoliang. \| The ocean there is beautiful. | · | generated example sentence (uses only app vocab + allowed words) |
| 9d772f8416e2 | proposed | Professional | 35 | 面试 | examples | · | 我明天有一个面试。 \| wǒ míngtiān yǒu yí ge miànshì. \| I have a job interview tomorrow. | · | generated example sentence (uses only app vocab + allowed words) |
| 698a6266c382 | proposed | Daily Life | 70 | 推荐 | examples | · | 你可以推荐一家餐厅吗？ \| Nǐ kěyǐ tuījiàn yì jiā cāntīng ma? \| Can you recommend a restaurant? | · | generated example sentence (uses only app vocab + allowed words) |
| d02eb70ebcfe | proposed | Descriptions | 20 | 干净 | examples | · | 厨房很干净。 \| Chúfáng hěn gānjìng. \| The kitchen is very clean. | · | generated example sentence (uses only app vocab + allowed words) |
| 8567b4fee456 | proposed | Activities | 31 | 听 | examples | · | 你听，外面下雨了。 \| Nǐ tīng, wàimiàn xiàyǔ le. \| Listen, it's raining outside. | · | generated example sentence (uses only app vocab + allowed words) |
| 0dba59f4a4e4 | proposed | Professional | 4 | 中医 | english | TCM (traditional Chinese medicine) | TCM (traditional Chinese medicine) / TCM doctor | medium | The measure word 位 only fits the 'TCM doctor' sense, which the gloss omits; 中医 commonly means a practitioner (看中医). |
| 4a048fa60d59 | proposed | Body | 13 | 中医 | english | TCM (traditional Chinese medicine) | TCM (traditional Chinese medicine) / TCM doctor | medium | The measure word 位 only fits the 'TCM doctor' sense, which the gloss omits; 中医 commonly means a practitioner (看中医). |
| ea724e40732e | proposed | Professional | 4 | 中医 | examples | · | 我去看中医。 \| Wǒ qù kàn zhōngyī. \| I'm going to see a TCM doctor. | · | generated example sentence (uses only app vocab + allowed words) |
| 8572f2a1995a | proposed | Daily Life | 2 | 下午 | examples | · | 我下午有空。 \| wǒ xiàwǔ yǒu kòng. \| I'm free this afternoon. | · | generated example sentence (uses only app vocab + allowed words) |
| ef448826c7f9 | proposed | Directions | 43 | 换乘 | examples | · | 我在这个地铁站换乘。 \| Wǒ zài zhège dìtiězhàn huànchéng. \| I transfer at this subway station. | · | generated example sentence (uses only app vocab + allowed words) |
| c2cc3d13b8f5 | proposed | Directions | 36 | 南 | examples | · | 地铁站在公园南边。 \| Dìtiězhàn zài gōngyuán nánbian. \| The subway station is on the south side of the park. | · | generated example sentence (uses only app vocab + allowed words) |
| 96b1b894c08c | proposed | Descriptions | 44 | 银色 | examples | · | 我爸爸的车是银色的。 \| wǒ bàba de chē shì yínsè de. \| My dad's car is silver. | · | generated example sentence (uses only app vocab + allowed words) |
| 893ffc995d51 | proposed | Objects | 12 | 手机 | examples | · | 这是我的新手机。 \| Zhè shì wǒ de xīn shǒujī. \| This is my new phone. | · | generated example sentence (uses only app vocab + allowed words) |
| 753d6d07de80 | proposed | Descriptions | 75 | 方便 | examples | · | 坐地铁很方便。 \| Zuò dìtiě hěn fāngbiàn. \| Taking the subway is convenient. | · | generated example sentence (uses only app vocab + allowed words) |
| 6152ec3f20f9 | proposed | Directions | 14 | 东 | examples | · | 公园在学校东边。 \| Gōngyuán zài xuéxiào dōngbian. \| The park is east of the school. | · | generated example sentence (uses only app vocab + allowed words) |
| 0d6801f88278 | proposed | Familiar People | 44 | 表白 | type | VOV | verb | medium | 表白 (express + state clearly) is not a verb-object compound; it is an ordinary verb, used as 跟/向某人表白. |
| 1ba2dc4f5125 | proposed | Familiar People | 44 | 表白 | examples | · | 他昨天跟她表白了。 \| Tā zuótiān gēn tā biǎobái le. \| He confessed his feelings to her yesterday. | · | generated example sentence (uses only app vocab + allowed words) |
| 87207034742e | proposed | Descriptions | 84 | 挤 | examples | · | 早上的地铁很挤。 \| Zǎoshang de dìtiě hěn jǐ. \| The subway is really crowded in the morning. | · | generated example sentence (uses only app vocab + allowed words) |
| 548434a0fb5a | proposed | Professional | 21 | 工作 | examples | · | 我想找一份新工作。 \| Wǒ xiǎng zhǎo yí fèn xīn gōngzuò. \| I want to find a new job. | · | generated example sentence (uses only app vocab + allowed words) |
| 4fb824ebcdb5 | proposed | Daily Life | 37 | 对不起 | examples | · | 对不起，我迟到了。 \| duìbuqǐ, wǒ chídào le. \| Sorry, I'm late. | · | generated example sentence (uses only app vocab + allowed words) |
| 4b7b52f866b1 | proposed | Professional | 20 | 休假 | examples | · | 经理现在在休假。 \| Jīnglǐ xiànzài zài xiūjià. \| The manager is on leave right now. | · | generated example sentence (uses only app vocab + allowed words) |
| 2595bdba3c5f | proposed | Descriptions | 81 | 奇怪 | examples | · | 他今天有点儿奇怪。 \| Tā jīntiān yǒudiǎnr qíguài. \| He's a bit strange today. | · | generated example sentence (uses only app vocab + allowed words) |
| 2228d1196a91 | proposed | Daily Life | 66 | 需要 | examples | · | 我需要一个新手机。 \| Wǒ xūyào yí ge xīn shǒujī. \| I need a new phone. | · | generated example sentence (uses only app vocab + allowed words) |
| 6f5f1043cb0c | proposed | Professional | 3 | 医生 | examples | · | 我妈妈是医生。 \| Wǒ māma shì yīshēng. \| My mom is a doctor. | · | generated example sentence (uses only app vocab + allowed words) |
| 829fcbb10bd1 | proposed | Objects | 45 | 桌子 | examples | · | 这张桌子很大。 \| zhè zhāng zhuōzi hěn dà. \| This table is very big. | · | generated example sentence (uses only app vocab + allowed words) |
| e11d671ef2cb | proposed | Professional | 14 | 出差 | examples | · | 我爸爸明天要出差。 \| Wǒ bàba míngtiān yào chūchāi. \| My dad is going on a business trip tomorrow. | · | generated example sentence (uses only app vocab + allowed words) |
| 1d47d50397b2 | proposed | Activities | 22 | 观察 | examples | · | 我在观察那只猫。 \| Wǒ zài guānchá nà zhī māo. \| I'm watching that cat closely. | · | generated example sentence (uses only app vocab + allowed words) |
| 3e350dcd3a13 | proposed | Descriptions | 71 | 高 | examples | · | 我哥哥很高。 \| Wǒ gēge hěn gāo. \| My older brother is tall. | · | generated example sentence (uses only app vocab + allowed words) |
| f537021ce7a9 | proposed | Professional | 6 | 收银员 | examples | · | 那个收银员很忙。 \| Nà ge shōuyínyuán hěn máng. \| That cashier is very busy. | · | generated example sentence (uses only app vocab + allowed words) |
| e16d5debbcaf | proposed | Daily Life | 8 | 早饭 | examples | · | 妈妈在做早饭。 \| māma zài zuò zǎofàn. \| Mom is making breakfast. | · | generated example sentence (uses only app vocab + allowed words) |
| 4635594ed971 | proposed | Daily Life | 7 | 生日 | examples | · | 今天是我的生日。 \| jīntiān shì wǒ de shēngrì. \| Today is my birthday. | · | generated example sentence (uses only app vocab + allowed words) |
| d5ec41d4ec31 | proposed | Daily Life | 9 | 中国电视剧 | pinyin | zhōngguó diànshìjù | Zhōngguó diànshìjù | low | 中国 is a proper noun, so its pinyin is normally capitalized. |
| 5205824be09e | proposed | Daily Life | 9 | 中国电视剧 | examples | · | 我在看一部中国电视剧。 \| wǒ zài kàn yí bù Zhōngguó diànshìjù. \| I'm watching a Chinese drama. | · | generated example sentence (uses only app vocab + allowed words) |
| e1f6f4aa0e25 | proposed | Daily Life | 22 | 我来吧 | examples | · | 我来吧，你休息吧。 \| Wǒ lái ba, nǐ xiūxi ba. \| I've got it — you take a rest. | · | generated example sentence (uses only app vocab + allowed words) |
| e7f4d2681490 | proposed | Body | 24 | 肩膀 | examples | · | 我的肩膀很疼。 \| Wǒ de jiānbǎng hěn téng. \| My shoulder really hurts. | · | generated example sentence (uses only app vocab + allowed words) |
| ca9472352c43 | proposed | Transition Words | 77 | 怪不得 | examples | · | 怪不得你很累，你昨天加班了。 \| guàibude nǐ hěn lèi, nǐ zuótiān jiābān le. \| No wonder you're tired, you worked overtime yesterday. | · | generated example sentence (uses only app vocab + allowed words) |
| ecb490a80297 | proposed | Transition Words | 39 | 跟 | examples | · | 我跟朋友去公园了。 \| Wǒ gēn péngyou qù gōngyuán le. \| I went to the park with a friend. | · | generated example sentence (uses only app vocab + allowed words) |
| e97ce99a2384 | proposed | Daily Life | 18 | 我没看见 | examples | · | 钥匙在哪儿？我没看见。 \| Yàoshi zài nǎr? Wǒ méi kànjiàn. \| Where are the keys? I didn't see them. | · | generated example sentence (uses only app vocab + allowed words) |
| 0d0c7f7fbc90 | proposed | Body | 57 | 减肥 | examples | · | 我要减肥。 \| Wǒ yào jiǎnféi. \| I want to lose weight. | · | generated example sentence (uses only app vocab + allowed words) |
| a23edfe61dde | proposed | Transition Words | 80 | 一定 | english | certain | definitely / surely / must | medium | As an adverb, 一定 means 'definitely / surely / must'. The gloss 'certain' reads as an adjective and is misleading. |
| 183d2c04b967 | proposed | Transition Words | 80 | 一定 | examples | · | 你一定要休息。 \| nǐ yídìng yào xiūxi. \| You really must get some rest. | · | generated example sentence (uses only app vocab + allowed words) |
| 7aadfb087700 | proposed | Directions | 2 | 面 | examples | · | 钥匙在桌子上面。 \| Yàoshi zài zhuōzi shàngmiàn. \| The keys are on the table. | · | generated example sentence (uses only app vocab + allowed words) |
| b26438656d95 | proposed | Places | 27 | 健身房 | examples | · | 我经常去健身房健身。 \| Wǒ jīngcháng qù jiànshēnfáng jiànshēn. \| I often go to the gym to work out. | · | generated example sentence (uses only app vocab + allowed words) |
| a810579fdeab | proposed | Objects | 23 | 水果 | examples | · | 这里的水果很新鲜。 \| Zhèlǐ de shuǐguǒ hěn xīnxian. \| The fruit here is very fresh. | · | generated example sentence (uses only app vocab + allowed words) |
| cd30e8f04f28 | proposed | Body | 40 | 耳朵 | examples | · | 我的耳朵有点儿疼。 \| Wǒ de ěrduo yǒudiǎnr téng. \| My ear hurts a bit. | · | generated example sentence (uses only app vocab + allowed words) |
| 0d6cf1b0f313 | proposed | Body | 38 | 嘴 | measure_word | · | 张 (zhāng) | high | 张 is the standard measure word for mouths (一张嘴). |
| 945f1f31f38b | proposed | Body | 38 | 嘴 | examples | · | 我的嘴很疼。 \| Wǒ de zuǐ hěn téng. \| My mouth hurts a lot. | · | generated example sentence (uses only app vocab + allowed words) |
| f42aaa97538d | proposed | Familiar People | 18 | 离婚 | type | verb | VOV | medium | 离婚 is a separable verb-object compound (e.g. 离过婚). |
| 3fb4ff84b58b | proposed | Familiar People | 18 | 离婚 | examples | · | 他们离婚了。 \| tāmen líhūn le. \| They got divorced. | · | generated example sentence (uses only app vocab + allowed words) |
| eddaf76913a3 | proposed | Daily Life | 92 | 周末 | examples | · | 这个周末你有空吗？ \| zhège zhōumò nǐ yǒu kòng ma? \| Are you free this weekend? | · | generated example sentence (uses only app vocab + allowed words) |
| ec31fa7b4460 | proposed | Activities | 34 | 做午饭 | examples | · | 妈妈在厨房做午饭。 \| Māma zài chúfáng zuò wǔfàn. \| Mom is making lunch in the kitchen. | · | generated example sentence (uses only app vocab + allowed words) |
| faf7a9025fb3 | proposed | Activities | 16 | 散步 | type | verb | VOV | medium | 散步 is a separable verb-object compound (散 + 步, e.g. 散散步, 散了一会儿步), like 跑步. |
| 632d00c232c4 | proposed | Activities | 16 | 散步 | examples | · | 我们去公园散步吧。 \| Wǒmen qù gōngyuán sànbù ba. \| Let's go for a walk in the park. | · | generated example sentence (uses only app vocab + allowed words) |
| 89da8575fc60 | proposed | Directions | 4 | 对面 | english | across | across from / opposite | low | 对面 is a location word meaning 'opposite / across from'. Bare 'across' could be read as the verb sense 'to cross'. |
| 6b0d8a2ea653 | proposed | Directions | 4 | 对面 | examples | · | 银行在超市对面。 \| Yínháng zài chāoshì duìmiàn. \| The bank is across from the grocery store. | · | generated example sentence (uses only app vocab + allowed words) |
| 23ba1ce372c2 | proposed | Places | 60 | 动物园 | examples | · | 周末我们去动物园吧。 \| Zhōumò wǒmen qù dòngwùyuán ba. \| Let's go to the zoo this weekend. | · | generated example sentence (uses only app vocab + allowed words) |
| a9a5f97c23be | proposed | Places | 38 | 图书馆 | examples | · | 我在图书馆看书。 \| wǒ zài túshūguǎn kànshū. \| I read at the library. | · | generated example sentence (uses only app vocab + allowed words) |
| 06a1a276364d | proposed | Daily Life | 20 | 我不知道 | examples | · | 他在哪儿？我不知道。 \| Tā zài nǎr? Wǒ bù zhīdào. \| Where is he? I don't know. | · | generated example sentence (uses only app vocab + allowed words) |
| d193b246abff | proposed | Activities | 44 | 开车 | examples | · | 你会开车吗？ \| nǐ huì kāichē ma? \| Can you drive? | · | generated example sentence (uses only app vocab + allowed words) |
| a052d346838a | proposed | Daily Life | 56 | 忘 | examples | · | 我忘了他的电话号码。 \| wǒ wàng le tā de diànhuà hàomǎ. \| I forgot his phone number. | · | generated example sentence (uses only app vocab + allowed words) |
| 99e4ebd251f4 | proposed | Descriptions | 3 | 大约 | examples | · | 从这里到机场大约一个小时。 \| Cóng zhèlǐ dào jīchǎng dàyuē yí ge xiǎoshí. \| It's about an hour from here to the airport. | · | generated example sentence (uses only app vocab + allowed words) |
| ae0b8c519082 | proposed | Body | 28 | 头 | examples | · | 我的头有点儿疼。 \| Wǒ de tóu yǒudiǎnr téng. \| My head hurts a little. | · | generated example sentence (uses only app vocab + allowed words) |
| f7610ccb686e | proposed | Body | 49 | 咳嗽 | examples | · | 我昨天晚上咳嗽得很厉害。 \| Wǒ zuótiān wǎnshang késou de hěn lìhai. \| I was coughing really badly last night. | · | generated example sentence (uses only app vocab + allowed words) |
| d322d3db7f4a | proposed | Directions | 24 | 前面 | examples | · | 前面有一个公交站。 \| Qiánmiàn yǒu yí ge gōngjiāozhàn. \| There's a bus stop up ahead. | · | generated example sentence (uses only app vocab + allowed words) |
| 70c2d6b65ff5 | proposed | Body | 3 | 过敏 | english | allergic | to be allergic | low | Card is typed as a verb; the gloss should reflect the verb use (对……过敏 = to be allergic to). |
| f3def0c4fd7c | proposed | Body | 3 | 过敏 | examples | · | 我对猫过敏。 \| wǒ duì māo guòmǐn. \| I'm allergic to cats. | · | generated example sentence (uses only app vocab + allowed words) |
| b87c5ead66e7 | proposed | Professional | 7 | 服务员 | examples | · | 服务员，我们要两碗米饭。 \| Fúwùyuán, wǒmen yào liǎng wǎn mǐfàn. \| Waiter, we'd like two bowls of rice. | · | generated example sentence (uses only app vocab + allowed words) |
| a258cfa91763 | proposed | Transition Words | 81 | 还 | examples | · | 他还在睡觉。 \| tā hái zài shuìjiào. \| He's still sleeping. | · | generated example sentence (uses only app vocab + allowed words) |
| 85662ad684b6 | proposed | Professional | 15 | 工人 | examples | · | 这家公司有三百个工人。 \| Zhè jiā gōngsī yǒu sān bǎi ge gōngrén. \| This company has three hundred workers. | · | generated example sentence (uses only app vocab + allowed words) |
| 8716de361449 | proposed | Body | 5 | 金色头发 | examples | · | 她有一头金色头发。 \| tā yǒu yì tóu jīnsè tóufa. \| She has blonde hair. | · | generated example sentence (uses only app vocab + allowed words) |
| 86ff651535f0 | proposed | Activities | 8 | 聊天 | type | verb | VOV | medium | 聊天 is a separable verb-object compound (e.g. 聊了一会儿天). |
| 46b45cfbe566 | proposed | Activities | 8 | 聊天 | examples | · | 我们在咖啡店聊天。 \| Wǒmen zài kāfēidiàn liáotiān. \| We're chatting at a café. | · | generated example sentence (uses only app vocab + allowed words) |
| 2b1c5de0859e | proposed | Descriptions | 6 | 无聊 | examples | · | 这个电影很无聊。 \| Zhège diànyǐng hěn wúliáo. \| This movie is boring. | · | generated example sentence (uses only app vocab + allowed words) |
| 5345c03bafb4 | proposed | Places | 48 | 公园 | examples | · | 我们去公园散步吧。 \| wǒmen qù gōngyuán sànbù ba. \| Let's go for a walk in the park. | · | generated example sentence (uses only app vocab + allowed words) |
| 1b08312ce9f8 | proposed | Professional | 8 | 保安 | english | doorman | security guard / doorman | medium | 保安 literally means security guard; 'doorman' alone is misleading, as the notes themselves explain. |
| f6ab4ddbfb5f | proposed | Professional | 8 | 保安 | examples | · | 楼下的保安认识我。 \| Lóuxià de bǎo'ān rènshi wǒ. \| The security guard downstairs knows me. | · | generated example sentence (uses only app vocab + allowed words) |
| 1bc165444a93 | proposed | Descriptions | 67 | 快 | examples | · | 地铁很快。 \| Dìtiě hěn kuài. \| The subway is fast. | · | generated example sentence (uses only app vocab + allowed words) |
| 75ded8f72a67 | proposed | Food | 3 | 菠菜 | measure_word | · | 把 (bǎ) | medium | Leafy vegetables like spinach are commonly counted by the bunch with 把 (or 棵 for a single plant). |
| 1379e7c7a07c | proposed | Food | 3 | 菠菜 | examples | · | 这儿的菠菜很便宜。 \| zhèr de bōcài hěn piányi. \| The spinach here is cheap. | · | generated example sentence (uses only app vocab + allowed words) |
| a3f81c82df9b | proposed | Descriptions | 88 | 所有 | examples | · | 所有的衣服都很贵。 \| suǒyǒu de yīfu dōu hěn guì. \| All the clothes are expensive. | · | generated example sentence (uses only app vocab + allowed words) |
| 8f6479e2181e | proposed | Directions | 18 | 下楼 | examples | · | 我下楼买咖啡。 \| Wǒ xiàlóu mǎi kāfēi. \| I'm going downstairs to buy coffee. | · | generated example sentence (uses only app vocab + allowed words) |
| 5d6e225996a3 | proposed | Body | 7 | 你多休息 | examples | · | 你多休息，注意身体。 \| nǐ duō xiūxi, zhùyì shēntǐ. \| Get some rest and take care of yourself. | · | generated example sentence (uses only app vocab + allowed words) |
| 686568a60a6b | proposed | Body | 19 | 背疼 | type | adjective | phrase | low | 背疼 is a subject + predicate combination ("back hurts"), not a single adjective; it works more like a phrase, the same as 头疼/肚子疼. |
| 0c7888cf9041 | proposed | Body | 19 | 背疼 | examples | · | 我今天背疼，不去健身房。 \| Wǒ jīntiān bèiténg, bú qù jiànshēnfáng. \| My back hurts today, so I'm not going to the gym. | · | generated example sentence (uses only app vocab + allowed words) |
| 606b6d978d76 | proposed | Descriptions | 13 | 差不多 | examples | · | 我们差不多到了。 \| Wǒmen chàbuduō dào le. \| We're almost there. | · | generated example sentence (uses only app vocab + allowed words) |
| 48bb29cd2b14 | proposed | Places | 59 | 火车站 | examples | · | 火车站在市中心。 \| Huǒchēzhàn zài shìzhōngxīn. \| The train station is downtown. | · | generated example sentence (uses only app vocab + allowed words) |
| e72905af5255 | proposed | Familiar People | 15 | 恋爱 | examples | · | 他们恋爱了。 \| Tāmen liàn'ài le. \| They've started dating. | · | generated example sentence (uses only app vocab + allowed words) |
| 379f45910418 | proposed | Objects | 2 | 半个小时 | examples | · | 我等了你半个小时。 \| Wǒ děng le nǐ bàn ge xiǎoshí. \| I waited for you for half an hour. | · | generated example sentence (uses only app vocab + allowed words) |
| a65797822079 | proposed | Objects | 30 | 钱 | examples | · | 我没有钱。 \| wǒ méiyǒu qián. \| I don't have any money. | · | generated example sentence (uses only app vocab + allowed words) |
| ffac46230227 | proposed | Activities | 45 | 骑车 | examples | · | 我骑车去上班。 \| wǒ qíchē qù shàngbān. \| I ride my bike to work. | · | generated example sentence (uses only app vocab + allowed words) |
| e8cef0f73ac0 | proposed | Activities | 24 | 做爱 | english | sex | to have sex | medium | 做爱 is a verb-object compound meaning 'to have sex', not the noun 'sex' (which is 性). |
| 6fc3c4ddd51a | proposed | Activities | 24 | 做爱 | examples | · | 他们结婚以前没有做爱。 \| Tāmen jiéhūn yǐqián méiyǒu zuò'ài. \| They didn't have sex before they got married. | · | generated example sentence (uses only app vocab + allowed words) |
| c9c1f7e30494 | proposed | Directions | 6 | 后 | examples | · | 我家后面有一个公园。 \| Wǒ jiā hòumiàn yǒu yí ge gōngyuán. \| There's a park behind my home. | · | generated example sentence (uses only app vocab + allowed words) |
| 0a7a6113d595 | proposed | Directions | 42 | 打车 | examples | · | 我们打车去机场吧。 \| Wǒmen dǎchē qù jīchǎng ba. \| Let's take a taxi to the airport. | · | generated example sentence (uses only app vocab + allowed words) |
| 5c94469617af | proposed | Activities | 52 | 发消息 | examples | · | 到了给我发消息。 \| dào le gěi wǒ fā xiāoxi. \| Text me when you arrive. | · | generated example sentence (uses only app vocab + allowed words) |
| 411690ef6859 | proposed | Places | 6 | 蛋糕店 | examples | · | 我家旁边有一家蛋糕店。 \| Wǒ jiā pángbiān yǒu yì jiā dàngāo diàn. \| There's a bakery next to my home. | · | generated example sentence (uses only app vocab + allowed words) |
| 4b89e5f59836 | proposed | Professional | 34 | 裁员 | examples | · | 公司裁员了。 \| gōngsī cáiyuán le. \| The company laid people off. | · | generated example sentence (uses only app vocab + allowed words) |
| 40b0a5a35197 | proposed | Places | 45 | 小区 | examples | · | 我住的小区很安静。 \| wǒ zhù de xiǎoqū hěn ānjìng. \| The residential compound I live in is very quiet. | · | generated example sentence (uses only app vocab + allowed words) |
| e65db181795c | proposed | Daily Life | 5 | 都可以 | examples | · | 喝什么都可以。 \| hē shénme dōu kěyǐ. \| I'm fine with anything to drink. | · | generated example sentence (uses only app vocab + allowed words) |
| 0ff68c304b95 | proposed | Directions | 7 | 后面 | examples | · | 我在你后面。 \| Wǒ zài nǐ hòumiàn. \| I'm behind you. | · | generated example sentence (uses only app vocab + allowed words) |
| 41799c96c2fa | proposed | Body | 32 | 心情不好 | examples | · | 我今天心情不好。 \| Wǒ jīntiān xīnqíng bù hǎo. \| I'm in a bad mood today. | · | generated example sentence (uses only app vocab + allowed words) |
| 042f68c1378e | proposed | Familiar People | 22 | 求婚 | type | verb | VOV | medium | 求婚 is a separable verb-object compound (e.g. 求过婚). |
| 52b6a250f5c5 | proposed | Familiar People | 22 | 求婚 | examples | · | 他求婚了。 \| tā qiúhūn le. \| He proposed. | · | generated example sentence (uses only app vocab + allowed words) |
| f5ab881c39b2 | proposed | Descriptions | 66 | 容易 | examples | · | 做饭很容易。 \| Zuòfàn hěn róngyì. \| Cooking is easy. | · | generated example sentence (uses only app vocab + allowed words) |
| e3db6c0e00dd | proposed | Descriptions | 46 | 黄色 | examples | · | 这个包是黄色的。 \| Zhège bāo shì huángsè de. \| This bag is yellow. | · | generated example sentence (uses only app vocab + allowed words) |
| 84677dcb35a0 | proposed | Directions | 44 | 往左拐 | examples | · | 到路口往左拐。 \| Dào lùkǒu wǎng zuǒ guǎi. \| Turn left when you reach the intersection. | · | generated example sentence (uses only app vocab + allowed words) |
| c09610655fbd | proposed | Objects | 27 | 首饰 | measure_word | 个 (gè) | 件 (jiàn) | medium | Pieces of jewelry are normally counted with 件 (一件首饰). 个 is uncommon for this noun. |
| 2e2184e39465 | proposed | Objects | 27 | 首饰 | examples | · | 她的首饰很漂亮。 \| Tā de shǒushi hěn piàoliang. \| Her jewelry is beautiful. | · | generated example sentence (uses only app vocab + allowed words) |
| a90eb7174aa2 | proposed | Body | 12 | 注意身体 | examples | · | 你要注意身体。 \| Nǐ yào zhùyì shēntǐ. \| You need to take care of yourself. | · | generated example sentence (uses only app vocab + allowed words) |
| 3613c0ec2a92 | proposed | Transition Words | 38 | 还是 | examples | · | 你要茶还是咖啡？ \| Nǐ yào chá háishì kāfēi? \| Do you want tea or coffee? | · | generated example sentence (uses only app vocab + allowed words) |
| 0ce4fe168c30 | proposed | Directions | 45 | 往右拐 | examples | · | 到公园往右拐。 \| Dào gōngyuán wǎng yòu guǎi. \| Turn right when you get to the park. | · | generated example sentence (uses only app vocab + allowed words) |
| ec8753c8d5a2 | proposed | Descriptions | 58 | 好看 | examples | · | 这部电影真好看。 \| Zhè bù diànyǐng zhēn hǎokàn. \| This movie is really good. | · | generated example sentence (uses only app vocab + allowed words) |
| fa1ecbfd7d7e | proposed | Familiar People | 20 | 约会 | examples | · | 我们明天约会。 \| wǒmen míngtiān yuēhuì. \| We're going on a date tomorrow. | · | generated example sentence (uses only app vocab + allowed words) |
| 79bf8cea7666 | proposed | Objects | 18 | 狗 | examples | · | 他们的狗很可爱。 \| Tāmen de gǒu hěn kě'ài. \| Their dog is really cute. | · | generated example sentence (uses only app vocab + allowed words) |
| e02c06e7899a | proposed | Transition Words | 40 | 和 | examples | · | 我有一只猫和一只狗。 \| Wǒ yǒu yì zhī māo hé yì zhī gǒu. \| I have a cat and a dog. | · | generated example sentence (uses only app vocab + allowed words) |
| 4c018da0a79a | proposed | Objects | 6 | 床 | measure_word | 个 (gè) | 张 (zhāng) | medium | The standard measure word for 床 is 张. 个 is heard in casual speech, but 张 is the one learners should know. |
| 8128aee1303f | proposed | Objects | 6 | 床 | examples | · | 这张床很舒服。 \| Zhè zhāng chuáng hěn shūfu. \| This bed is very comfortable. | · | generated example sentence (uses only app vocab + allowed words) |
| 0ac614ee376b | proposed | Transition Words | 43 | 多久 | examples | · | 你在这里住了多久？ \| Nǐ zài zhèlǐ zhù le duō jiǔ? \| How long have you lived here? | · | generated example sentence (uses only app vocab + allowed words) |
| b399bf4e22f6 | proposed | Body | 25 | 腿 | examples | · | 他的腿很长。 \| Tā de tuǐ hěn cháng. \| His legs are really long. | · | generated example sentence (uses only app vocab + allowed words) |
| ec44dc90733f | proposed | Activities | 15 | 停车 | type | verb | VOV | medium | 停车 is a separable verb-object compound (停 + 车, e.g. 停好车). |
| b1f715e39609 | proposed | Activities | 15 | 停车 | examples | · | 这里可以停车吗？ \| Zhèlǐ kěyǐ tíngchē ma? \| Can I park here? | · | generated example sentence (uses only app vocab + allowed words) |
| 9bd0b7c2f734 | proposed | Daily Life | 73 | 看 | examples | · | 你看，那是我的猫。 \| Nǐ kàn, nà shì wǒ de māo. \| Look, that's my cat. | · | generated example sentence (uses only app vocab + allowed words) |
| d29d0ab3efa0 | proposed | Objects | 46 | 茶 | examples | · | 我想喝一杯茶。 \| wǒ xiǎng hē yì bēi chá. \| I'd like to drink a cup of tea. | · | generated example sentence (uses only app vocab + allowed words) |
| 75ded2070ea6 | proposed | Activities | 18 | 游泳 | type | verb | VOV | low | 游泳 is a separable verb-object compound (游了一个小时泳, 游个泳), like 跳舞 and 跑步. |
| 1057bd81ac94 | proposed | Activities | 18 | 游泳 | examples | · | 我周末常常去游泳。 \| Wǒ zhōumò chángcháng qù yóuyǒng. \| I often go swimming on weekends. | · | generated example sentence (uses only app vocab + allowed words) |
| 15765260a6a1 | proposed | Directions | 21 | 怎么走 | examples | · | 去地铁站怎么走？ \| Qù dìtiězhàn zěnme zǒu? \| How do I get to the subway station? | · | generated example sentence (uses only app vocab + allowed words) |
| e860c07c21c7 | proposed | Transition Words | 10 | 然后 | examples | · | 我们吃饭，然后去看电影。 \| wǒmen chīfàn, ránhòu qù kàn diànyǐng. \| We'll eat, and then go see a movie. | · | generated example sentence (uses only app vocab + allowed words) |
| 892c0f16d9ee | proposed | Professional | 32 | 加班 | examples | · | 我今天要加班。 \| wǒ jīntiān yào jiābān. \| I have to work overtime today. | · | generated example sentence (uses only app vocab + allowed words) |
| 180fb9ca7e6f | proposed | Professional | 11 | 会员 | examples | · | 我是这家健身房的会员。 \| Wǒ shì zhè jiā jiànshēnfáng de huìyuán. \| I'm a member of this gym. | · | generated example sentence (uses only app vocab + allowed words) |
| 093fbc2b3339 | proposed | Body | 16 | 看病 | examples | · | 我明天去医院看病。 \| Wǒ míngtiān qù yīyuàn kànbìng. \| I'm going to the hospital to see a doctor tomorrow. | · | generated example sentence (uses only app vocab + allowed words) |
| f9541fc9f88c | proposed | Familiar People | 9 | 女性朋友 | examples | · | 我有几个女性朋友。 \| Wǒ yǒu jǐ ge nǚxìng péngyou. \| I have a few female friends. | · | generated example sentence (uses only app vocab + allowed words) |
| 6b9bdbf67bff | proposed | Daily Life | 75 | 睡觉 | examples | · | 我很累，我要睡觉了。 \| Wǒ hěn lèi, wǒ yào shuìjiào le. \| I'm really tired; I'm going to sleep. | · | generated example sentence (uses only app vocab + allowed words) |
| b66cd2a6ca75 | proposed | Places | 34 | 房子 | examples | · | 他们买了一套新房子。 \| Tāmen mǎi le yí tào xīn fángzi. \| They bought a new house. | · | generated example sentence (uses only app vocab + allowed words) |
| 45e42abee3c6 | proposed | Professional | 27 | 律师 | examples | · | 我需要找一个律师。 \| Wǒ xūyào zhǎo yí ge lǜshī. \| I need to find a lawyer. | · | generated example sentence (uses only app vocab + allowed words) |
| fcb29a06dd50 | proposed | Daily Life | 15 | 多少钱 | examples | · | 这杯奶茶多少钱？ \| Zhè bēi nǎichá duōshao qián? \| How much is this cup of milk tea? | · | generated example sentence (uses only app vocab + allowed words) |
| 9001a17d15e2 | proposed | Activities | 48 | 打游戏 | examples | · | 我弟弟晚上常常打游戏。 \| wǒ dìdi wǎnshang chángcháng dǎ yóuxì. \| My younger brother often plays games in the evening. | · | generated example sentence (uses only app vocab + allowed words) |
| 029dc3d65d84 | proposed | Daily Life | 86 | 排队 | examples | · | 我们在排队买票。 \| wǒmen zài páiduì mǎi piào. \| We're waiting in line to buy tickets. | · | generated example sentence (uses only app vocab + allowed words) |
| ccf42ab2f4e7 | proposed | Transition Words | 26 | 以前 / 过去 | examples | · | 我以前住在乡下。 \| Wǒ yǐqián zhù zài xiāngxia. \| I used to live in the countryside. | · | generated example sentence (uses only app vocab + allowed words) |
| a7cbbacf7a9b | proposed | Descriptions | 59 | 好玩 | examples | · | 这个游戏很好玩。 \| Zhège yóuxì hěn hǎowán. \| This game is a lot of fun. | · | generated example sentence (uses only app vocab + allowed words) |
| ef08ab3d4456 | proposed | Activities | 13 | 搬家 | type | verb | VOV | medium | 搬家 is a separable verb-object compound (搬 + 家, e.g. 搬过三次家). |
| 643240eaa32f | proposed | Activities | 13 | 搬家 | examples | · | 我明天搬家。 \| Wǒ míngtiān bānjiā. \| I'm moving tomorrow. | · | generated example sentence (uses only app vocab + allowed words) |
| b71ce1df885f | proposed | Professional | 5 | 老师 | examples | · | 我们的老师很厉害。 \| Wǒmen de lǎoshī hěn lìhai. \| Our teacher is really great. | · | generated example sentence (uses only app vocab + allowed words) |
| 2b61083a9ce6 | proposed | Descriptions | 76 | 甜 | examples | · | 这杯奶茶太甜了。 \| Zhè bēi nǎichá tài tián le. \| This cup of milk tea is too sweet. | · | generated example sentence (uses only app vocab + allowed words) |
| bfca9dc12656 | proposed | Verbs | 4 | 脱鞋 | examples | · | 在朋友家要脱鞋。 \| Zài péngyou jiā yào tuō xié. \| You have to take off your shoes at a friend's place. | · | generated example sentence (uses only app vocab + allowed words) |
| 9ad6928f4cd8 | proposed | Descriptions | 62 | 漂亮 | examples | · | 你的衣服真漂亮。 \| Nǐ de yīfu zhēn piàoliang. \| Your clothes are really pretty. | · | generated example sentence (uses only app vocab + allowed words) |
| d67909dcdbf3 | proposed | Daily Life | 32 | 其他 | examples | · | 这个太贵了，有其他的吗？ \| Zhège tài guì le, yǒu qítā de ma? \| This one is too expensive — do you have any others? | · | generated example sentence (uses only app vocab + allowed words) |
| ee94a7979af4 | proposed | Professional | 26 | 护士 | examples | · | 这家医院的护士很好。 \| Zhè jiā yīyuàn de hùshi hěn hǎo. \| The nurses at this hospital are very good. | · | generated example sentence (uses only app vocab + allowed words) |
| 582b439fc48e | proposed | Descriptions | 18 | 害怕 | examples | · | 我害怕狗。 \| Wǒ hàipà gǒu. \| I'm scared of dogs. | · | generated example sentence (uses only app vocab + allowed words) |
| 7ee9092f218d | proposed | Descriptions | 57 | 好吃 | examples | · | 这家餐厅的烤鸭很好吃。 \| Zhè jiā cāntīng de kǎoyā hěn hǎochī. \| The roast duck at this restaurant is delicious. | · | generated example sentence (uses only app vocab + allowed words) |
| 63964aa8a586 | proposed | Familiar People | 5 | 同学 | examples | · | 他是我的同学。 \| Tā shì wǒ de tóngxué. \| He's my classmate. | · | generated example sentence (uses only app vocab + allowed words) |
| 25c4e466fb90 | proposed | Daily Life | 33 | 其他人 | examples | · | 其他人在哪儿？ \| Qítārén zài nǎr? \| Where is everyone else? | · | generated example sentence (uses only app vocab + allowed words) |
| a4b852a177df | proposed | Transition Words | 41 | 真的吗 | examples | · | 真的吗？你要结婚了？ \| Zhēn de ma? Nǐ yào jiéhūn le? \| Really? You're getting married? | · | generated example sentence (uses only app vocab + allowed words) |
| 63aca71d441b | proposed | Descriptions | 12 | 热闹 | examples | · | 这个市场很热闹。 \| Zhège shìchǎng hěn rènao. \| This market is very lively. | · | generated example sentence (uses only app vocab + allowed words) |
| 9a33c3012b33 | proposed | Descriptions | 69 | 长 | examples | · | 她的头发很长。 \| Tā de tóufa hěn cháng. \| Her hair is long. | · | generated example sentence (uses only app vocab + allowed words) |
| bf7bf552edf0 | proposed | Objects | 38 | 米饭 | examples | · | 我要两碗米饭。 \| wǒ yào liǎng wǎn mǐfàn. \| I'd like two bowls of rice. | · | generated example sentence (uses only app vocab + allowed words) |
| 5bd5e7f8b0a6 | proposed | Places | 29 | 走廊 | examples | · | 这条走廊很长。 \| Zhè tiáo zǒuláng hěn cháng. \| This hallway is very long. | · | generated example sentence (uses only app vocab + allowed words) |
| 612fca070ede | proposed | Body | 20 | 休息 | examples | · | 我很累，想休息。 \| Wǒ hěn lèi, xiǎng xiūxi. \| I'm really tired and want to rest. | · | generated example sentence (uses only app vocab + allowed words) |
| 2f9793323896 | proposed | Descriptions | 15 | 湿透 | examples | · | 我的衣服湿透了。 \| Wǒ de yīfu shītòu le. \| My clothes are soaked. | · | generated example sentence (uses only app vocab + allowed words) |
| 7e0876d94362 | proposed | Transition Words | 67 | 另一方面 | examples | · | 这个公寓很便宜,另一方面,它离市中心很远。 \| Zhège gōngyù hěn piányi, lìng yì fāngmiàn, tā lí shìzhōngxīn hěn yuǎn. \| This apartment is cheap; on the other hand, it's far from downtown. | · | generated example sentence (uses only app vocab + allowed words) |
| feaa7868148e | proposed | Descriptions | 31 | 灰色 | examples | · | 我的电脑是灰色的。 \| wǒ de diànnǎo shì huīsè de. \| My computer is gray. | · | generated example sentence (uses only app vocab + allowed words) |
| 39dbdd70128b | proposed | Places | 15 | 楼 | measure_word | 个 (gè) | 栋 (dòng) | medium | The standard classifier for a building (楼) is 栋 (or 座); 个 is heard colloquially but is not the one to teach. |
| 2ed925f2d951 | proposed | Places | 15 | 楼 | examples | · | 我住在三楼。 \| Wǒ zhù zài sān lóu. \| I live on the third floor. | · | generated example sentence (uses only app vocab + allowed words) |
| ccea4619bf43 | proposed | Activities | 21 | 端午节 | examples | · | 端午节我要跟家人吃饭。 \| Duānwǔjié wǒ yào gēn jiārén chīfàn. \| I'm having a meal with my family for the Dragon Boat Festival. | · | generated example sentence (uses only app vocab + allowed words) |
| 49184b695bc7 | proposed | Daily Life | 87 | 洗 | examples | · | 我在洗盘子。 \| wǒ zài xǐ pánzi. \| I'm washing the plates. | · | generated example sentence (uses only app vocab + allowed words) |
| e1a4fdf288f1 | proposed | Daily Life | 52 | 打扫 | examples | · | 我今天要打扫厨房。 \| wǒ jīntiān yào dǎsǎo chúfáng. \| I need to clean the kitchen today. | · | generated example sentence (uses only app vocab + allowed words) |
| 59529cfa4e77 | proposed | Professional | 13 | 放假 | examples | · | 学校明天放假。 \| Xuéxiào míngtiān fàngjià. \| School goes on break tomorrow. | · | generated example sentence (uses only app vocab + allowed words) |
| 6c76c714efad | proposed | Places | 13 | 书店 | examples | · | 我常常去那家书店看书。 \| Wǒ chángcháng qù nà jiā shūdiàn kànshū. \| I often go to that bookstore to read. | · | generated example sentence (uses only app vocab + allowed words) |
| 4780dc5d2630 | proposed | Daily Life | 71 | 记得 | examples | · | 你还记得我吗？ \| Nǐ hái jìde wǒ ma? \| Do you still remember me? | · | generated example sentence (uses only app vocab + allowed words) |
| f65f96e98035 | proposed | Body | 43 | 胳膊 | examples | · | 我的胳膊受伤了。 \| Wǒ de gēbo shòushāng le. \| I hurt my arm. | · | generated example sentence (uses only app vocab + allowed words) |
| bbbcaf8b9069 | proposed | Descriptions | 47 | 奇幻 | examples | · | 这部奇幻电影很好看。 \| Zhè bù qíhuàn diànyǐng hěn hǎokàn. \| This fantasy movie is really good. | · | generated example sentence (uses only app vocab + allowed words) |
| 19ab27e56636 | proposed | Descriptions | 35 | 浅蓝色 | examples | · | 我有一双浅蓝色的鞋。 \| wǒ yǒu yì shuāng qiǎn lánsè de xié. \| I have a pair of light blue shoes. | · | generated example sentence (uses only app vocab + allowed words) |
| deff9d90086b | proposed | Descriptions | 2 | 有点儿 | examples | · | 今天有点儿冷。 \| Jīntiān yǒudiǎnr lěng. \| It's a bit cold today. | · | generated example sentence (uses only app vocab + allowed words) |
| 615c52225a37 | proposed | Activities | 2 | 合菜 | english | family-style eating | shared dishes / group set meal | low | In Mainland usage 合菜 usually means a shared set of dishes (or the northern stir-fry 炒合菜); the practice of communal dining itself is more often called 合餐 (hécān). |
| 078486fa5dab | proposed | Activities | 2 | 合菜 | examples | · | 这家餐厅的合菜很好吃。 \| Zhè jiā cāntīng de hécài hěn hǎochī. \| This restaurant's shared dishes are delicious. | · | generated example sentence (uses only app vocab + allowed words) |
| cb5a2c3fd9fb | proposed | Descriptions | 26 | 深 | examples | · | 这里的海很深。 \| zhèlǐ de hǎi hěn shēn. \| The ocean here is very deep. | · | generated example sentence (uses only app vocab + allowed words) |
| 653a67594b92 | proposed | Body | 17 | 吃药 | examples | · | 你吃药了吗？ \| Nǐ chī yào le ma? \| Have you taken your medicine? | · | generated example sentence (uses only app vocab + allowed words) |
| 6c26c47865b5 | proposed | Activities | 32 | 做 | examples | · | 你在做什么？ \| Nǐ zài zuò shénme? \| What are you doing? | · | generated example sentence (uses only app vocab + allowed words) |
| d0272735c40f | proposed | Directions | 32 | 上面 | examples | · | 手机在桌子上面。 \| Shǒujī zài zhuōzi shàngmiàn. \| The phone is on the table. | · | generated example sentence (uses only app vocab + allowed words) |
| f70e859a3240 | proposed | Descriptions | 40 | 淡黄色 | examples | · | 这条淡黄色的裤子很好看。 \| zhè tiáo dàn huángsè de kùzi hěn hǎokàn. \| These pale yellow pants look great. | · | generated example sentence (uses only app vocab + allowed words) |
| 711cc965649d | proposed | Descriptions | 9 | 冷 | examples | · | 今天很冷。 \| Jīntiān hěn lěng. \| It's cold today. | · | generated example sentence (uses only app vocab + allowed words) |
| 613102cf0075 | proposed | Descriptions | 77 | 咸 | examples | · | 这个汤有点儿咸。 \| Zhège tāng yǒudiǎnr xián. \| This soup is a bit salty. | · | generated example sentence (uses only app vocab + allowed words) |
| 3923c238a221 | proposed | Familiar People | 41 | 最好的朋友 | examples | · | 他是我最好的朋友。 \| Tā shì wǒ zuì hǎo de péngyou. \| He is my best friend. | · | generated example sentence (uses only app vocab + allowed words) |
| d6567e60b49a | proposed | Activities | 20 | 单身派对 | examples | · | 我要参加朋友的单身派对。 \| Wǒ yào cānjiā péngyou de dānshēn pàiduì. \| I'm going to my friend's bachelor party. | · | generated example sentence (uses only app vocab + allowed words) |
| 8680728d9d68 | proposed | Directions | 27 | 地图 | examples | · | 我买了一张地图。 \| Wǒ mǎi le yì zhāng dìtú. \| I bought a map. | · | generated example sentence (uses only app vocab + allowed words) |
| 5daa2dea7ccb | proposed | Daily Life | 29 | 中学生 | examples | · | 我妹妹是中学生。 \| Wǒ mèimei shì zhōngxuéshēng. \| My younger sister is a middle school student. | · | generated example sentence (uses only app vocab + allowed words) |
| abb637cd4c9b | proposed | Daily Life | 26 | 让我想想 | examples | · | 我们去哪儿吃饭？让我想想。 \| Wǒmen qù nǎr chīfàn? Ràng wǒ xiǎngxiang. \| Where should we go to eat? Let me think. | · | generated example sentence (uses only app vocab + allowed words) |
| 37421c4a1e95 | proposed | Activities | 38 | 唱歌 | examples | · | 我们去唱歌吧！ \| wǒmen qù chànggē ba! \| Let's go sing! | · | generated example sentence (uses only app vocab + allowed words) |
| 20185ae9a3f6 | proposed | Activities | 61 | 足球 | measure_word | · | 个 (gè) | low | Nouns should list a measure word; 个 is used for the ball (一个足球). Matches take 场 (一场足球比赛). |
| 1c435841e20f | proposed | Activities | 61 | 足球 | examples | · | 周末我跟朋友看足球。 \| Zhōumò wǒ gēn péngyou kàn zúqiú. \| I watch soccer with friends on the weekend. | · | generated example sentence (uses only app vocab + allowed words) |
| dcc8b362179c | proposed | Descriptions | 23 | 蓝色 | examples | · | 他的车是蓝色的。 \| Tā de chē shì lánsè de. \| His car is blue. | · | generated example sentence (uses only app vocab + allowed words) |
| 082dc964ea25 | proposed | Objects | 9 | 书 | examples | · | 这本书很有意思。 \| Zhè běn shū hěn yǒu yìsi. \| This book is really interesting. | · | generated example sentence (uses only app vocab + allowed words) |
| a94eee013169 | proposed | Body | 30 | 眼镜 | examples | · | 我的眼镜在哪儿？ \| Wǒ de yǎnjìng zài nǎr? \| Where are my glasses? | · | generated example sentence (uses only app vocab + allowed words) |
| ccbeb28131ee | proposed | Descriptions | 89 | 都 | examples | · | 我们都是同学。 \| wǒmen dōu shì tóngxué. \| We are all classmates. | · | generated example sentence (uses only app vocab + allowed words) |
| c563a3bc4501 | proposed | Transition Words | 23 | 已经 | examples | · | 我已经吃饭了。 \| Wǒ yǐjīng chīfàn le. \| I've already eaten. | · | generated example sentence (uses only app vocab + allowed words) |
| e67ff0add6f4 | proposed | Body | 56 | 运动 | examples | · | 我常常运动。 \| Wǒ chángcháng yùndòng. \| I exercise often. | · | generated example sentence (uses only app vocab + allowed words) |
| 800289d4917b | proposed | Descriptions | 55 | 便宜 | examples | · | 这个市场的水果很便宜。 \| Zhège shìchǎng de shuǐguǒ hěn piányi. \| The fruit at this market is cheap. | · | generated example sentence (uses only app vocab + allowed words) |
| 0c8690571213 | proposed | Transition Words | 5 | 有时候 | english | sometimes/when have time | sometimes | high | 有时候 only means 'sometimes'; 'when (I) have time' is 有空的时候, as the note itself explains. |
| 3328f5e23366 | proposed | Transition Words | 5 | 有时候 | examples | · | 我有时候在家工作。 \| wǒ yǒu shíhou zài jiā gōngzuò. \| I sometimes work from home. | · | generated example sentence (uses only app vocab + allowed words) |
| 0cc699c171ec | proposed | Transition Words | 19 | 那次 | examples | · | 那次我们去了海滩。 \| Nà cì wǒmen qù le hǎitān. \| That time we went to the beach. | · | generated example sentence (uses only app vocab + allowed words) |

### Claude flags (no automatic fix)

| hanzi | field | current | note | conf. |
|---|---|---|---|---|
| 咱们 | measure_word | 个 (gè) | 咱们 is a pronoun; pronouns don't take measure words. | high |
| 会议 | notes | 会 alone is a bound form living inside 开会 (to have a meeting) and 会员; 会议 is the free-standing noun. 会 also separately means "can/know how to." | 会 is not a bound form in the meeting sense; it is used freely as a noun, as in 我下午有个会. | medium |
| 下 | notes | A bound locative — it needs 面 or 边 to stand alone: 下面 / 下边 = below. 下 by itself is the verb "to go down" (下楼, 下班, 下雨). | 下 is regularly used as a locative right after a noun (桌子下, 楼下). The note implies it only works as a verb without 面/边. | low |
| 一个小时 | measure_word | 个 (gè) | The card is a time expression, not a noun; the 个 is already part of the phrase, so a measure_word entry doesn't belong here. | high |
| 水 | notes | Basic noun, root of 水果 (fruit) and 游泳 (to swim). | 游泳 does not contain the character 水; it only shares the water radical 氵, so calling 水 its 'root' is misleading. | medium |
| 长路口 | hanzi | 长路口 | 路口 means 'intersection', not 'block'. 长路口 is not a standard term. Colloquially a block is counted with 路口 (e.g. 走两个路口), and the formal word is 街区. | medium |
| 火车 | notes | 火 (fire) + 车 (vehicle) — a holdover name from steam trains. Measure words: 列 (liè) for the train as a whole, 辆 for a single carriage, 趟 or 班 for a scheduled service. | The standard measure word for a train carriage is 节 (一节车厢), not 辆. | medium |
| 短路口 | hanzi | 短路口 | Not a standard term, since 路口 means 'intersection'. 短路 also means 'short circuit', so the string is easily misread. | medium |
| 打扫 | notes | Split from your combined "打扫 / 收拾" entry. Usually implies sweeping/cleaning a space (floors, surfaces). | The note contains an editorial remark about the deck's history that isn't useful to the learner. | medium |
| 合菜 | notes | 合 (to combine) + 菜 (dishes) — shared dishes eaten together, as opposed to individual plates. Your note describes this as 大家一起吃 ("everyone eats together"), which is more a descriptive phrase than a fixed term. | The second sentence is leftover editorial commentary addressed to the card author, not learner-facing content. | high |

<details><summary>Warnings (2)</summary>

| where | hanzi | field | warning |
|---|---|---|---|
| Objects row 4 | 一个小时 | measure_word | measure word on a 'time' |
| cross-tab | 家 | hanzi | 2 different cards share this hanzi (Measure Words, Places): check for a typo splitting one card in two |

</details>
