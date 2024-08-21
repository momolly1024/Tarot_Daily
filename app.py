from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextSendMessage, MessageEvent, TextMessage
import random
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# LINE Bot API and Webhook Handler initialization os.getenv('CHANNEL_ACCESS_TOKEN')
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
handler =  WebhookHandler(os.getenv('CHANNEL_SECRET'))

love = [
    {"cardName":'愚者(The Fool)正位', "cardDes":'愛情中，愚者正位代表一種新鮮感與冒險精神。你可能會遇到一個讓你感覺充滿可能性的人，或許這段關係充滿了探索與冒險，但要注意保持真實與自我。'},
    {"cardName":'愚者(The Fool)逆位', "cardDes":'愛情中，愚者逆位可能預示著輕率的行為或不成熟的態度。你或對方可能在感情中表現得不夠負責任，需避免不切實際的幻想或衝動行為。'},
    {"cardName":'魔術師(The Magician)正位', "cardDes":'愛情中，魔術師正位象徵著實現你的願望與目標的能力。這張牌顯示你或你的伴侶擁有良好的溝通與創造力，能夠在關係中達成共識並創造美好未來。'},
    {"cardName":'魔術師(The Magician)逆位', "cardDes":'愛情中，魔術師逆位可能暗示著誠信的缺失或試圖操控他人。這張牌提醒你在感情中保持真誠，不要被表面的魅力或花言巧語所迷惑。'},
    {"cardName":'女祭司(The High Priestess)正位', "cardDes":'愛情中，女祭司正位表示直覺和內在智慧的作用。你或你的伴侶可能會感受到深層次的情感聯繫，並且在關係中要信任你的直覺與內心的指引。'},
    {"cardName":'女祭司(The High Priestess)逆位', "cardDes":'愛情中，女祭司逆位可能預示著對直覺的忽視或內在衝突。這張牌提醒你要重視內心的感受，避免忽略或壓抑自己的情感需求。'},
    {"cardName":'皇后(The Empress)正位', "cardDes":'愛情中，皇后正位象徵著滋養與關懷。這張牌預示著充滿愛與支持的關係，你與伴侶之間的情感深厚，可能會迎來幸福和繁榮的時期。'},
    {"cardName":'皇后(The Empress)逆位', "cardDes":'愛情中，皇后逆位可能代表關係中的冷漠或缺乏關懷。這張牌提醒你檢視自己在感情中的需求，並試圖重新建立情感上的聯繫與支持。'},
    {"cardName":'皇帝(The Emperor)正位', "cardDes":'愛情中，皇帝正位象徵穩定與安全感。這張牌預示著你或你的伴侶在關係中擁有主導地位，能夠提供穩固的支持與保護。'},
    {"cardName":'皇帝(The Emperor)逆位', "cardDes":'愛情中，皇帝逆位可能暗示著控制欲或權力鬥爭。這張牌提醒你在關係中要注意權力的平衡，避免過度控制或壓迫對方。'},
    {"cardName":'教皇(The Hierophant)正位', "cardDes":'愛情中，教皇正位代表傳統與穩定。這張牌預示著你與伴侶之間的關係可能會遵循傳統的價值觀，並尋求長期的承諾與穩定。'},
    {"cardName":'教皇(The Hierophant)逆位', "cardDes":'愛情中，教皇逆位可能暗示著對傳統的反叛或價值觀的衝突。這張牌提醒你在感情中保持開放的心態，尋找符合你們價值觀的方式來解決問題。'},
    {"cardName":'戀人(The Lovers)正位', "cardDes":'愛情中，戀人正位象徵著深厚的情感聯繫與和諧的關係。這張牌預示著你與伴侶之間有強烈的吸引力與愛情，並可能面臨重要的選擇。'},
    {"cardName":'戀人(The Lovers)逆位', "cardDes":'愛情中，戀人逆位可能暗示著關係中的矛盾或選擇的困難。這張牌提醒你要解決感情中的問題，尋求和諧與理解以克服困難。'},
    {"cardName":'戰車(The Chariot)正位', "cardDes":'愛情中，戰車正位象徵著意志力與決心。這張牌預示著你在感情中展現出強烈的目標感和努力，並且能夠克服困難實現關係的進展。'},
    {"cardName":'戰車(The Chariot)逆位', "cardDes":'愛情中，戰車逆位可能代表失去方向或控制。這張牌提醒你檢視你在感情中的目標，避免衝動行事或與伴侶間出現矛盾。'},
    {"cardName":'力量(Strength)正位', "cardDes":'愛情中，力量正位象徵著勇氣與耐心。這張牌預示著你在關係中展現出堅韌的力量與愛，並且能夠克服困難以保持關係的穩定。'},
    {"cardName":'力量(Strength)逆位', "cardDes":'愛情中，力量逆位可能暗示著內心的不安或缺乏自信。這張牌提醒你要尋求支持與鼓勵，並重新建立自信以改善關係。'},
    {"cardName":'隱士(The Hermit)正位', "cardDes":'愛情中，隱士正位代表尋求內在的智慧與靜默的時間。這張牌預示著你或你的伴侶需要一些獨處的時間來反思與理解自己，並在感情中尋求深層次的連結。'},
    {"cardName":'隱士(The Hermit)逆位', "cardDes":'愛情中，隱士逆位可能預示著孤立與隔閡。這張牌提醒你在關係中保持溝通，避免自我封閉或忽略伴侶的需求。'},
    {"cardName":'命運之輪(The Wheel of Fortune)正位', "cardDes":'愛情中，命運之輪正位象徵著變化與機會的到來。這張牌預示著你可能會經歷關係中的轉折點或新的機遇，保持開放的心態迎接變化。'},
    {"cardName":'命運之輪(The Wheel of Fortune)逆位', "cardDes":'愛情中，命運之輪逆位可能代表運氣的不穩定或反覆。這張牌提醒你在面對感情中的變化時保持穩定，並接受命運的起伏。'},
    {"cardName":'正義(Justice)正位', "cardDes":'愛情中，正義正位象徵著公平與誠實。這張牌預示著你與伴侶之間的關係需要建立在相互尊重與理解的基礎上，並且在處理問題時尋求公平的解決方案。'},
    {"cardName":'正義(Justice)逆位', "cardDes":'愛情中，正義逆位可能暗示著不公平或失衡。這張牌提醒你檢視關係中的問題，避免不公平的對待或不誠實的行為。'},
    {"cardName":'吊人(The Hanged Man)正位', "cardDes":'愛情中，吊人正位代表等待與放手。這張牌預示著你可能需要在感情中放慢腳步，重新評估關係，並學會放下過去以迎接新的開始。'},
    {"cardName":'吊人(The Hanged Man)逆位', "cardDes":'愛情中，吊人逆位可能預示著停滯不前或難以做出決定。這張牌提醒你在感情中要勇於改變與調整，避免陷入僵局或消極的態度。'},
    {"cardName":'死神(Death)正位', "cardDes":'愛情中，死神正位象徵著結束與新生。這張牌預示著你可能會經歷一段關係的結束或重大的變革，並迎來新的開始或成長。'},
    {"cardName":'死神(Death)逆位', "cardDes":'愛情中，死神逆位可能代表拒絕變化或無法放下過去。這張牌提醒你接受變化的必要性，並尋求放下過去以迎接新的機遇。'},
    {"cardName":'節制(Temperance)正位', "cardDes":'愛情中，節制正位象徵著平衡與和諧。這張牌預示著你在感情中能夠找到平衡，並通過合作與調和達成共同目標。'},
    {"cardName":'節制(Temperance)逆位', "cardDes":'愛情中，節制逆位可能暗示著關係中的不平衡或衝突。這張牌提醒你檢視感情中的問題，並尋求調整與和解。'},
    {"cardName":'魔鬼(The Devil)正位', "cardDes":'愛情中，魔鬼正位象徵著誘惑與束縛。這張牌預示著你可能面臨感情中的挑戰，涉及依賴或不健康的關係，需要解放自己並尋求真實的愛。'},
    {"cardName":'魔鬼(The Devil)逆位', "cardDes":'愛情中，魔鬼逆位可能代表擺脫束縛或克服挑戰。這張牌提醒你在感情中努力解脫困境，尋求健康與自由的關係。'},
    {"cardName":'塔(The Tower)正位', "cardDes":'愛情中，塔正位象徵著突然的變故與震撼。這張牌預示著你可能會經歷感情中的重大變化或衝突，需準備面對不預期的挑戰。'},
    {"cardName":'塔(The Tower)逆位', "cardDes":'愛情中，塔逆位可能暗示著避免或延遲變革。這張牌提醒你在感情中勇敢面對問題，並尋求變革以改善關係。'},
    {"cardName":'星星(The Star)正位', "cardDes":'愛情中，星星正位象徵希望與療癒。這張牌預示著你與伴侶之間有恢復的機會，並且關係充滿希望與正能量。'},
    {"cardName":'星星(The Star)逆位', "cardDes":'愛情中，星星逆位可能代表失望或缺乏信心。這張牌提醒你在感情中重新找到希望與信任，並避免對未來感到消極。'},
    {"cardName":'太陽(The Sun)正位', "cardDes":'愛情中，太陽正位象徵著幸福與光明。這張牌預示著你與伴侶之間的關係充滿了喜悅與和諧，並可能迎來幸福與成功的時期。'},
    {"cardName":'太陽(The Sun)逆位', "cardDes":'愛情中，太陽逆位可能暗示著短暫的挫折或不滿。這張牌提醒你在感情中尋求積極的改變，並保持對未來的樂觀。'},
    {"cardName":'審判(Judgement)正位', "cardDes":'愛情中，審判正位象徵著自我反省與重生。這張牌預示著你可能會重新評估感情，並在過去的經驗中學習與成長。'},
    {"cardName":'審判(Judgement)逆位', "cardDes":'愛情中，審判逆位可能代表不願面對過去或未能改變。這張牌提醒你在感情中正視過去的問題，並尋求解決與成長。'},
    {"cardName":'世界(The World)正位', "cardDes":'愛情中，世界正位象徵著圓滿與成就。這張牌預示著你在感情中達到了一個階段的完成，並享受了關係中的成功與滿足。'},
    {"cardName":'世界(The World)逆位', "cardDes":'愛情中，世界逆位可能暗示著未完成的目標或困境。這張牌提醒你在感情中尋求解決方案，並完成未完成的事情以迎接新的機遇。'},
    {"cardName":'權杖王牌(Ace of Wands)正位', "cardDes":'愛情中，權杖王牌正位代表著新的激情與創意。這張牌預示著你可能會迎來一段充滿活力與興奮的新關係或感情階段。'},
    {"cardName":'權杖王牌(Ace of Wands)逆位', "cardDes":'愛情中，權杖王牌逆位可能暗示著失去興奮或缺乏動力。這張牌提醒你在感情中重新尋找激情與動力，避免情感上的停滯。'},
    {"cardName":'權杖二(Ace of Wands)正位', "cardDes":'愛情中，權杖二正位象徵著決策與規劃。這張牌預示著你在感情中需要做出重要的選擇，並規劃未來的發展。'},
    {"cardName":'權杖二(Ace of Wands)逆位', "cardDes":'愛情中，權杖二逆位可能代表猶豫或計劃上的困難。這張牌提醒你在感情中避免拖延或決策上的困惑。'},
    {"cardName":'權杖三(Ace of Wands)正位', "cardDes":'愛情中，權杖三正位象徵著合作與展望。這張牌預示著你與伴侶之間有良好的合作機會，共同實現未來的目標。'},
    {"cardName":'權杖三(Ace of Wands)逆位', "cardDes":'愛情中，權杖三逆位可能暗示著合作上的障礙或缺乏遠見。這張牌提醒你在關係中尋求共同的目標與合作。'},
    {"cardName":'權杖四(Ace of Wands)正位', "cardDes":'愛情中，權杖四正位象徵著穩定與慶祝。這張牌預示著你與伴侶之間的關係穩定，並迎來了幸福與和諧的時期。'},
    {"cardName":'權杖四(Ace of Wands)逆位', "cardDes":'愛情中，權杖四逆位可能代表不穩定或缺乏慶祝。這張牌提醒你在感情中尋求穩定與慶祝的機會，避免情感上的起伏。'},
    {"cardName":'權杖五(Ace of Wands)正位', "cardDes":'愛情中，權杖五正位象徵著競爭與衝突。這張牌預示著你可能會面臨感情中的挑戰或競爭，需要尋求解決方案以達成和諧。'},
    {"cardName":'權杖五(Ace of Wands)逆位', "cardDes":'愛情中，權杖五逆位可能暗示著衝突的解決或爭鬥的結束。這張牌提醒你在關係中尋求和平與理解。'},
    {"cardName":'權杖六(Ace of Wands)正位', "cardDes":'愛情中，權杖六正位象徵著成功與榮耀。這張牌預示著你在感情中獲得了認可與成功，並迎來了一段令人驕傲的時期。'},
    {"cardName":'權杖六(Ace of Wands)逆位', "cardDes":'愛情中，權杖六逆位可能代表未能獲得認可或成功。這張牌提醒你在感情中尋求支持與認可，避免感到沮喪或失落。'},
    {"cardName":'權杖七(Ace of Wands)正位', "cardDes":'愛情中，權杖七正位象徵著堅持與挑戰。這張牌預示著你在感情中面臨挑戰，需要堅持自己的立場並努力解決問題。'},
    {"cardName":'權杖七(Ace of Wands)逆位', "cardDes":'愛情中，權杖七逆位可能代表放棄或不願面對挑戰。這張牌提醒你在感情中勇敢面對困難，並尋求解決方案。'},
    {"cardName":'權杖八(Ace of Wands)正位', "cardDes":'愛情中，權杖八正位象徵著迅速的進展與變化。這張牌預示著你在感情中會經歷快速的變化或進展，並迎來新的機遇。'},
    {"cardName":'權杖八(Ace of Wands)逆位', "cardDes":'愛情中，權杖八逆位可能暗示著進展的緩慢或延遲。這張牌提醒你在感情中保持耐心，並避免急於求成。'},
    {"cardName":'權杖九(Ace of Wands)正位', "cardDes":'愛情中，權杖九正位象徵著防禦與保護。這張牌預示著你在感情中需要保護自己或關係，並面對挑戰與壓力。'},
    {"cardName":'權杖九(Ace of Wands)逆位', "cardDes":'愛情中，權杖九逆位可能代表防禦上的困難或不安。這張牌提醒你在關係中尋求支持與穩定，避免過度防禦。'},
    {"cardName":'權杖十(Ace of Wands)正位', "cardDes":'愛情中，權杖十正位象徵著責任與壓力。這張牌預示著你在感情中承擔了許多責任，需要處理好壓力並尋求平衡。'},
    {"cardName":'權杖十(Ace of Wands)逆位', "cardDes":'愛情中，權杖十逆位可能暗示著過度負擔或責任感的問題。這張牌提醒你在感情中尋求解脫，避免過度承擔壓力。'},
    {"cardName":'權杖侍者(Page of Wands)正位', "cardDes":'愛情中，權杖侍者正位象徵著探索與學習。這張牌預示著你可能會遇到一段充滿學習與探索的關係，並對未來充滿期待。'},
    {"cardName":'權杖侍者(Page of Wands)逆位', "cardDes":'愛情中，權杖侍者逆位可能代表缺乏方向或不成熟的態度。這張牌提醒你在感情中保持成熟，避免不切實際的幻想。'},
    {"cardName":'權杖騎士(Knight of Wands)正位', "cardDes":'愛情中，權杖騎士正位象徵著激情與冒險。這張牌預示著你可能會經歷一段充滿激情與冒險的關係，並需要勇敢地追求你的目標。'},
    {"cardName":'權杖騎士(Knight of Wands)逆位', "cardDes":'愛情中，權杖騎士逆位可能暗示著衝動或缺乏承諾。這張牌提醒你在感情中保持穩定，避免衝動行為。'},
    {"cardName":'權杖皇后(Queen of Wands)正位', "cardDes":'愛情中，權杖皇后正位象徵著自信與魅力。這張牌預示著你在感情中展現出強大的吸引力與魅力，並能夠吸引到合適的伴侶。'},
    {"cardName":'權杖皇后(Queen of Wands)逆位', "cardDes":'愛情中，權杖皇后逆位可能代表自信的缺乏或情感上的挑戰。這張牌提醒你在感情中尋求自我價值的提升，避免情感上的不穩定。'},
    {"cardName":'權杖國王(King of Wands)正位', "cardDes":'愛情中，權杖國王正位象徵著領導與決策。這張牌預示著你在感情中展現出強大的領導力，並能夠做出明智的決策以促進關係的發展。'},
    {"cardName":'權杖國王(King of Wands)逆位', "cardDes":'愛情中，權杖國王逆位可能暗示著控制欲或權力的問題。這張牌提醒你在感情中尋求平衡，避免過度控制或壓迫對方。'},
    {"cardName":'聖杯王牌(Ace of Cups)正位', "cardDes":'愛情中，聖杯王牌正位象徵著新的情感開始。這張牌預示著你可能會迎來一段充滿愛與情感的新關係，並經歷感情上的充實與滿足。'},
    {"cardName":'聖杯王牌(Ace of Cups)逆位', "cardDes":'愛情中，聖杯王牌逆位可能暗示著情感的封閉或困難。這張牌提醒你在感情中尋求情感的開放與療癒，避免壓抑自己的情感需求。'},
    {"cardName":'聖杯二(Ace of Cups)正位', "cardDes":'愛情中，聖杯二正位象徵著互相吸引與合作。這張牌預示著你與伴侶之間有良好的情感聯繫與合作，並能夠共同實現感情上的目標。'},
    {"cardName":'聖杯二(Ace of Cups)逆位', "cardDes":'愛情中，聖杯二逆位可能代表情感上的不和諧或關係中的矛盾。這張牌提醒你在感情中尋求理解與和解，避免情感上的對立。'},
    {"cardName":'聖杯三(Ace of Cups)正位', "cardDes":'愛情中，聖杯三正位象徵著慶祝與喜悅。這張牌預示著你在感情中將迎來充滿快樂與喜悅的時期，並與伴侶共享幸福。'},
    {"cardName":'聖杯三(Ace of Cups)逆位', "cardDes":'愛情中，聖杯三逆位可能暗示著情感的失落或困境。這張牌提醒你在感情中尋求支持與療癒，避免孤獨或沮喪。'},
    {"cardName":'聖杯四(Ace of Cups)正位', "cardDes":'愛情中，聖杯四正位象徵著內在的反思與情感的重新評估。這張牌預示著你可能會對感情中的需求進行重新評估，並尋求情感上的滿足。'},
    {"cardName":'聖杯四(Ace of Cups)逆位', "cardDes":'愛情中，聖杯四逆位可能代表對感情的不滿或倦怠。這張牌提醒你在感情中尋求新的動力與滿足，避免對關係感到厭倦。'},
    {"cardName":'聖杯五(Ace of Cups)正位', "cardDes":'愛情中，聖杯五正位象徵著失落與接受。這張牌預示著你可能會經歷情感上的失落，但也能夠學會接受過去並尋求新的開始。'},
    {"cardName":'聖杯五(Ace of Cups)逆位', "cardDes":'愛情中，聖杯五逆位可能暗示著接受與療癒。這張牌提醒你在感情中尋求療癒，並放下過去的傷痛以迎接新的機遇。'},
    {"cardName":'聖杯六(Ace of Cups)正位', "cardDes":'愛情中，聖杯六正位象徵著回憶與懷舊。這張牌預示著你可能會重溫過去的情感經歷，並在關係中尋找過去的美好回憶。'},
    {"cardName":'聖杯六(Ace of Cups)逆位', "cardDes":'愛情中，聖杯六逆位可能代表對過去的困擾或無法放下。這張牌提醒你在感情中尋求放下過去，並專注於當下的幸福。'},
    {"cardName":'聖杯七(Ace of Cups)正位', "cardDes":'愛情中，聖杯七正位象徵著選擇與幻想。這張牌預示著你可能面臨感情中的選擇，並需要理性地對待幻想與現實。'},
    {"cardName":'聖杯七(Ace of Cups)逆位', "cardDes":'愛情中，聖杯七逆位可能暗示著清晰與實現。這張牌提醒你在感情中尋求清晰的目標，並避免陷入幻想或迷茫。'},
    {"cardName":'聖杯八(Ace of Cups)正位', "cardDes":'愛情中，聖杯八正位象徵著放手與尋求新的機會。這張牌預示著你可能會放下過去的感情，並尋求新的情感機會。'},
    {"cardName":'聖杯八(Ace of Cups)逆位', "cardDes":'愛情中，聖杯八逆位可能代表未能放手或困難。這張牌提醒你在感情中尋求釋放與放下，避免困在過去的情感中。'},
    {"cardName":'聖杯九(Ace of Cups)正位', "cardDes":'愛情中，聖杯九正位象徵著情感上的滿足與成就。這張牌預示著你在感情中獲得了滿足與幸福，並實現了情感上的目標。'},
    {"cardName":'聖杯九(Ace of Cups)逆位', "cardDes":'愛情中，聖杯九逆位可能暗示著情感上的不滿或失望。這張牌提醒你在感情中尋求滿足與平衡，避免對未來感到沮喪。'},
    {"cardName":'聖杯十(Ace of Cups)正位', "cardDes":'愛情中，聖杯十正位象徵著家庭與圓滿。這張牌預示著你在感情中獲得了家庭的圓滿與幸福，並享受了關係中的和諧。'},
    {"cardName":'聖杯十(Ace of Cups)逆位', "cardDes":'愛情中，聖杯十逆位可能代表家庭的困難或不和諧。這張牌提醒你在感情中尋求和諧與解決問題，避免家庭的衝突。'},
    {"cardName":'聖杯侍者(Page of Cups)正位', "cardDes":'愛情中，聖杯侍者正位象徵著情感的開放與表達。這張牌預示著你在感情中能夠表達自己的情感，並建立真誠的聯繫。'},
    {"cardName":'聖杯侍者(Page of Cups)逆位', "cardDes":'愛情中，聖杯侍者逆位可能暗示著情感上的困難或不成熟。這張牌提醒你在感情中保持成熟與開放，避免情感上的封閉。'},
    {"cardName":'聖杯騎士(Knight of Cups)正位', "cardDes":'愛情中，聖杯騎士正位象徵著浪漫與追求。這張牌預示著你可能會迎來一段浪漫的關係，並勇敢地追求你的情感目標。'},
    {"cardName":'聖杯騎士(Knight of Cups)逆位', "cardDes":'愛情中，聖杯騎士逆位可能代表浪漫的過度或情感上的困難。這張牌提醒你在感情中保持現實，避免浪漫上的過度幻想。'},
    {"cardName":'聖杯皇后(Queen of Cups)正位', "cardDes":'愛情中，聖杯皇后正位象徵著同情與理解。這張牌預示著你在感情中展現出深刻的情感理解與關懷，並能夠建立穩定的關係。'},
    {"cardName":'聖杯皇后(Queen of Cups)逆位', "cardDes":'愛情中，聖杯皇后逆位可能暗示著情感的困擾或情緒的失衡。這張牌提醒你在感情中尋求內心的平衡，避免情感上的不穩定。'},
    {"cardName":'聖杯國王(King of Cups)正位', "cardDes":'愛情中，聖杯國王正位象徵著情感的穩定與成熟。這張牌預示著你在感情中展現出成熟的情感與穩定的關係，並能夠有效地管理情感。'},
    {"cardName":'聖杯國王(King of Cups)逆位', "cardDes":'愛情中，聖杯國王逆位可能代表情感上的控制或不穩定。這張牌提醒你在感情中尋求平衡，避免情感上的控制或波動。'},
    {"cardName":'劍王牌(Ace of Swords)正位', "cardDes":'愛情中，劍王牌正位象徵著清晰與真相。這張牌預示著你在感情中將面對真實的情況，並能夠明確地理解感情中的問題。'},
    {"cardName":'劍王牌(Ace of Swords)逆位', "cardDes":'愛情中，劍王牌逆位可能暗示著混亂或誤解。這張牌提醒你在感情中尋求清晰與溝通，避免誤解或困惑。'},
    {"cardName":'劍二(Ace of Swords)正位', "cardDes":'愛情中，劍二正位象徵著選擇與平衡。這張牌預示著你在感情中需要做出重要的選擇，並尋求平衡的解決方案。'},
    {"cardName":'劍二(Ace of Swords)逆位', "cardDes":'愛情中，劍二逆位可能代表決策上的困難或矛盾。這張牌提醒你在感情中尋求清晰與平衡，避免陷入困惑或猶豫。'},
    {"cardName":'劍三(Ace of Swords)正位', "cardDes":'愛情中，劍三正位象徵著痛苦與分離。這張牌預示著你可能會經歷感情中的痛苦或分離，需要面對情感上的挑戰。'},
    {"cardName":'劍三(Ace of Swords)逆位', "cardDes":'愛情中，劍三逆位可能暗示著治癒或解決。這張牌提醒你在感情中尋求解決過去的問題，並努力治癒心靈。'},
    {"cardName":'劍四(Ace of Swords)正位', "cardDes":'愛情中，劍四正位象徵著休息與沉思。這張牌預示著你在感情中需要休息與反思，並在內心中尋求平靜與安慰。'},
    {"cardName":'劍四(Ace of Swords)逆位', "cardDes":'愛情中，劍四逆位可能代表焦慮或無法放鬆。這張牌提醒你在感情中尋求平靜，並避免過度的焦慮或壓力。'},
    {"cardName":'劍五(Ace of Swords)正位', "cardDes":'愛情中，劍五正位象徵著衝突與競爭。這張牌預示著你可能會面臨感情中的衝突或競爭，需要尋求解決方案以達成和諧。'},
    {"cardName":'劍五(Ace of Swords)逆位', "cardDes":'愛情中，劍五逆位可能暗示著衝突的解決或和解。這張牌提醒你在感情中尋求和平與理解，避免衝突的升級。'},
    {"cardName":'劍六(Ace of Swords)正位', "cardDes":'愛情中，劍六正位象徵著轉變與前進。這張牌預示著你在感情中將經歷變化，並需要放下過去的困擾，迎接新的開始。'},
    {"cardName":'劍六(Ace of Swords)逆位', "cardDes":'愛情中，劍六逆位可能代表未能放下過去或困難的前行。這張牌提醒你在感情中努力解決過去的問題，並尋求新的機會。'},
    {"cardName":'劍七(Ace of Swords)正位', "cardDes":'愛情中，劍七正位象徵著謹慎與策略。這張牌預示著你在感情中需要謹慎地處理問題，並尋求策略性的解決方案。'},
    {"cardName":'劍七(Ace of Swords)逆位', "cardDes":'愛情中，劍七逆位可能暗示著不誠實或策略上的困難。這張牌提醒你在感情中保持誠實，避免操縱或欺瞞。'},
    {"cardName":'劍八(Ace of Swords)正位', "cardDes":'愛情中，劍八正位象徵著束縛與限制。這張牌預示著你可能會感受到感情中的限制或困難，並需要尋找解脫的方法。'},
    {"cardName":'劍八(Ace of Swords)逆位', "cardDes":'愛情中，劍八逆位可能代表對束縛的突破或逃脫。這張牌提醒你在感情中努力擺脫困境，並尋求自由與解放。'},
    {"cardName":'劍九(Ace of Swords)正位', "cardDes":'愛情中，劍九正位象徵著焦慮與憂慮。這張牌預示著你可能會面臨感情中的焦慮或擔憂，需要尋求情感上的安慰與支持。'},
    {"cardName":'劍九(Ace of Swords)逆位', "cardDes":'愛情中，劍九逆位可能暗示著解脫與釋放。這張牌提醒你在感情中努力放下焦慮，並尋求內心的平靜與放鬆。'},
    {"cardName":'劍十(Ace of Swords)正位', "cardDes":'愛情中，劍十正位象徵著結束與轉變。這張牌預示著你可能會經歷感情中的結束或重大變化，並需要迎接新的開始。'},
    {"cardName":'劍十(Ace of Swords)逆位', "cardDes":'愛情中，劍十逆位可能代表未能結束或困難的轉變。這張牌提醒你在感情中努力解決問題，避免被過去困擾。'},
    {"cardName":'劍侍者(Page of Swords)正位', "cardDes":'愛情中，劍侍者正位象徵著觀察與探索。這張牌預示著你可能會在感情中進行深入的探索與了解，並保持警覺與好奇心。'},
    {"cardName":'劍侍者(Page of Swords)逆位', "cardDes":'愛情中，劍侍者逆位可能暗示著謠言或衝突。這張牌提醒你在感情中保持冷靜，避免參與無謂的爭執或謠言。'},
    {"cardName":'劍騎士(Knight of Swords)正位', "cardDes":'愛情中，劍騎士正位象徵著迅速與果斷。這張牌預示著你在感情中會以果斷的方式行動，並迅速解決問題。'},
    {"cardName":'劍騎士(Knight of Swords)逆位', "cardDes":'愛情中，劍騎士逆位可能代表衝動或爭執。這張牌提醒你在感情中避免衝動行為，並尋求冷靜與理性。'},
    {"cardName":'劍皇后(Queen of Swords)正位', "cardDes":'愛情中，劍皇后正位象徵著明智與直覺。這張牌預示著你在感情中能夠清晰地了解情況，並做出明智的決策。'},
    {"cardName":'劍皇后(Queen of Swords)逆位', "cardDes":'愛情中，劍皇后逆位可能暗示著情感上的冷漠或誤解。這張牌提醒你在感情中保持溫暖與開放，避免冷漠與隔閡。'},
    {"cardName":'劍國王(King of Swords)正位', "cardDes":'愛情中，劍國王正位象徵著理智與公正。這張牌預示著你在感情中能夠以公正的態度面對問題，並做出理智的決策。'},
    {"cardName":'劍國王(King of Swords)逆位', "cardDes":'愛情中，劍國王逆位可能代表控制欲或誤解。這張牌提醒你在感情中尋求平衡，避免過度的控制或誤解對方。'},
    {"cardName":'硬幣王牌(Ace of Pentacles)正位', "cardDes":'愛情中，硬幣王牌正位象徵著實質的機遇與穩定。這張牌預示著你在感情中可能會迎來穩定的關係或實質的發展。'},
    {"cardName":'硬幣王牌(Ace of Pentacles)逆位', "cardDes":'愛情中，硬幣王牌逆位可能暗示著財務上的挑戰或不穩定。這張牌提醒你在感情中尋求穩定，並注意物質方面的問題。'},
    {"cardName":'硬幣二(Ace of Pentacles)正位', "cardDes":'愛情中，硬幣二正位象徵著平衡與適應。這張牌預示著你在感情中需要尋求平衡，並適應變化的情況。'},
    {"cardName":'硬幣二(Ace of Pentacles)逆位', "cardDes":'愛情中，硬幣二逆位可能代表混亂或困難的平衡。這張牌提醒你在感情中尋求穩定，並解決困擾。'},
    {"cardName":'硬幣三(Ace of Pentacles)正位', "cardDes":'愛情中，硬幣三正位象徵著合作與努力。這張牌預示著你在感情中通過合作與努力，能夠實現共同的目標。'},
    {"cardName":'硬幣三(Ace of Pentacles)逆位', "cardDes":'愛情中，硬幣三逆位可能暗示著合作上的問題或不和諧。這張牌提醒你在感情中尋求理解，並避免合作中的摩擦。'},
    {"cardName":'硬幣四(Ace of Pentacles)正位', "cardDes":'愛情中，硬幣四正位象徵著安全與保護。這張牌預示著你在感情中能夠建立穩定的基礎，並保護你的關係。'},
    {"cardName":'硬幣四(Ace of Pentacles)逆位', "cardDes":'愛情中，硬幣四逆位可能代表對安全感的焦慮或不安。這張牌提醒你在感情中尋求內心的平靜，避免過度擔憂。'},
    {"cardName":'硬幣五(Ace of Pentacles)正位', "cardDes":'愛情中，硬幣五正位象徵著困難與挑戰。這張牌預示著你在感情中可能會面臨困難，需要克服挑戰以實現幸福。'},
    {"cardName":'硬幣五(Ace of Pentacles)逆位', "cardDes":'愛情中，硬幣五逆位可能暗示著困境的解決或經濟上的改善。這張牌提醒你在感情中尋求支持，並努力解決問題。'},
    {"cardName":'硬幣六(Ace of Pentacles)正位', "cardDes":'愛情中，硬幣六正位象徵著慷慨與分享。這張牌預示著你在感情中能夠展現慷慨，並與伴侶分享幸福。'},
    {"cardName":'硬幣六(Ace of Pentacles)逆位', "cardDes":'愛情中，硬幣六逆位可能代表分享上的困難或不公平。這張牌提醒你在感情中尋求公平與平衡，避免自私或不公平的行為。'},
    {"cardName":'硬幣七(Ace of Pentacles)正位', "cardDes":'愛情中，硬幣七正位象徵著評估與等待。這張牌預示著你在感情中需要對關係進行評估，並耐心等待結果。'},
    {"cardName":'硬幣七(Ace of Pentacles)逆位', "cardDes":'愛情中，硬幣七逆位可能暗示著對未來的焦慮或等待的困難。這張牌提醒你在感情中保持耐心，並尋求支持。'},
    {"cardName":'硬幣八(Ace of Pentacles)正位', "cardDes":'愛情中，硬幣八正位象徵著努力與進步。這張牌預示著你在感情中通過努力與實踐，能夠取得進步和發展。'},
    {"cardName":'硬幣八(Ace of Pentacles)逆位', "cardDes":'愛情中，硬幣八逆位可能代表對工作的過度專注或忽視感情。這張牌提醒你在感情中尋求平衡，避免過度投入工作而忽略伴侶。'},
    {"cardName":'硬幣九(Ace of Pentacles)正位', "cardDes":'愛情中，硬幣九正位象徵著豐收與滿足。這張牌預示著你在感情中能夠獲得豐富的回報與滿足，並享受關係中的成果。'},
    {"cardName":'硬幣九(Ace of Pentacles)逆位', "cardDes":'愛情中，硬幣九逆位可能暗示著滿足感的缺乏或物質上的困難。這張牌提醒你在感情中尋求內心的滿足，並注意物質方面的問題。'},
    {"cardName":'硬幣十(Ace of Pentacles)正位', "cardDes":'愛情中，硬幣十正位象徵著家庭與長期穩定。這張牌預示著你在感情中建立了穩定的家庭基礎，並享受長期的幸福。'},
    {"cardName":'硬幣十(Ace of Pentacles)逆位', "cardDes":'愛情中，硬幣十逆位可能代表家庭的困難或經濟上的挑戰。這張牌提醒你在感情中尋求穩定，並解決家庭或財務上的問題。'},
    {"cardName":'硬幣侍者(Page of Pentacles)正位', "cardDes":'愛情中，硬幣侍者正位象徵著學習與實踐。這張牌預示著你在感情中將通過學習與實踐來提升關係，並尋求成長。'},
    {"cardName":'硬幣侍者(Page of Pentacles)逆位', "cardDes":'愛情中，硬幣侍者逆位可能暗示著不成熟或對感情的忽視。這張牌提醒你在感情中保持成熟，並避免對伴侶的不重視。'},
    {"cardName":'硬幣騎士(Knight of Pentacles)正位', "cardDes":'愛情中，硬幣騎士正位象徵著責任與穩定。這張牌預示著你在感情中能夠展現出負責任的態度，並建立穩定的關係。'},
    {"cardName":'硬幣騎士(Knight of Pentacles)逆位', "cardDes":'愛情中，硬幣騎士逆位可能代表缺乏動力或進展緩慢。這張牌提醒你在感情中保持積極，避免拖延或停滯不前。'},
    {"cardName":'硬幣皇后(Queen of Pentacles)正位', "cardDes":'愛情中，硬幣皇后正位象徵著關懷與實用。這張牌預示著你在感情中展現出實用的關懷，並能夠提供支持與安全感。'},
    {"cardName":'硬幣皇后(Queen of Pentacles)逆位', "cardDes":'愛情中，硬幣皇后逆位可能暗示著關懷上的不足或不實用。這張牌提醒你在感情中尋求實際的支持，避免過度理想化。'},
    {"cardName":'硬幣國王(King of Pentacles)正位', "cardDes":'愛情中，硬幣國王正位象徵著成功與穩定。這張牌預示著你在感情中能夠建立成功的關係，並享受穩定的幸福。'},
    {"cardName":'硬幣國王(King of Pentacles)逆位', "cardDes":'愛情中，硬幣國王逆位可能代表財務上的困難或控制欲。這張牌提醒你在感情中尋求平衡，避免物質上的問題影響關係。'}
    
    
]

fortune = [
    {"cardName":'愚者(The Fool)正位', "cardDes":'今天你可能會感受到一種新的開始，充滿冒險和探索的能量。勇敢地迎接挑戰，不要害怕未知。'},
    {"cardName":'愚者(The Fool)逆位', "cardDes":'今天你可能會感到不安或缺乏方向。注意不要盲目行事，建議在做決定前多加考慮。'},
    {"cardName":'魔術師(The Magician)正位', "cardDes":'你今天擁有實現目標的力量和資源。善用你的技能和能力，積極地追求你的夢想。'},
    {"cardName":'魔術師(The Magician)逆位', "cardDes":'今天可能會感到你的能力被限制或無法發揮。檢查是否存在誠信問題或有過度的自我欺騙。'},
    {"cardName":'女祭司(The High Priestess)正位', "cardDes":'今天是深入內心、自我反思的好時機。信任你的直覺，它將引領你走向正確的方向。'},
    {"cardName":'女祭司(The High Priestess)逆位', "cardDes":'你可能會感到迷茫或不確定。建議暫時放慢步伐，聆聽內心的聲音，避免外界的干擾。'},
    {"cardName":'皇后(The Empress)正位', "cardDes":'今天你可能會感受到豐富的創造力和豐盈。這是一個好時機來照顧自己和他人，享受生活的美好。'},
    {"cardName":'皇后(The Empress)逆位', "cardDes":'今天你可能會感到缺乏關懷或支持。試著找到平衡，不要過度依賴他人，照顧好自己。'},
    {"cardName":'皇帝(The Emperor)正位', "cardDes":'今天你可能會感受到穩定和控制的力量。你擁有制定計劃和建立秩序的能力，勇敢地展現領導力。'},
    {"cardName":'皇帝(The Emperor)逆位', "cardDes":'今天你可能會面臨權威或控制問題。建議避免強勢行事，學會妥協和調整策略。'},
    {"cardName":'教宗(The Hierophant)正位', "cardDes":'今天你可能會獲得智慧和指導。遵循傳統和固有的價值觀，尋求值得信賴的意見。'},
    {"cardName":'教宗(The Hierophant)逆位', "cardDes":'你可能會感到對常規或傳統的抵觸。挑戰既定的規則，尋找符合自己信念的新方法。'},
    {"cardName":'戀人(The Lovers)正位', "cardDes":'今天可能會有重要的情感或關係決定。這是一個選擇和和諧的時刻，注重誠實和理解。'},
    {"cardName":'戀人(The Lovers)逆位', "cardDes":'今天可能會面臨關係上的困難或選擇。避免衝動決策，試著從不同的角度看問題。'},
    {"cardName":'戰車(The Chariot)正位', "cardDes":'你今天擁有前進的動力和毅力。保持專注和決心，克服障礙，實現你的目標。'},
    {"cardName":'戰車(The Chariot)逆位', "cardDes":'今天你可能會感到失去方向或控制。調整你的策略，保持冷靜，避免過度的衝突。'},
    {"cardName":'力量(Strength)正位', "cardDes":'今天你可能會感受到內在的力量和勇氣。利用你的耐心和同情心，克服挑戰。'},
    {"cardName":'力量(Strength)逆位', "cardDes":'你可能會感到脆弱或不安。試著平衡內心的力量，不要被外界壓力所困擾。'},
    {"cardName":'隱士(The Hermit)正位', "cardDes":'今天是反思和尋求內心智慧的好時機。暫時隱退，尋找自我，接受內心的啟示。'},
    {"cardName":'隱士(The Hermit)逆位', "cardDes":'你可能會感到孤獨或封閉。嘗試與他人交流，打開內心的世界，尋求支持和理解。'},
    {"cardName":'命運之輪(The Wheel of Fortune)正位', "cardDes":'今天可能會有變化和機會的出現。接受這些變化，抓住機會，順應命運的潮流。'},
    {"cardName":'命運之輪(The Wheel of Fortune)逆位', "cardDes":'你可能會感到不穩定或面臨困難。這是重新評估和調整的時候，尋找新的方法來應對挑戰。'},
    {"cardName":'正義(Justice)正位', "cardDes":'今天是做出公平和正義的決定的時候。保持公正，遵循道德原則，處理問題。'},
    {"cardName":'正義(Justice)逆位', "cardDes":'你可能會面臨不公平或糾紛。檢查自己是否有偏見，尋找解決問題的公正方法。'},
    {"cardName":'吊人(The Hanged Man)正位', "cardDes":'今天可能需要放下固有的觀念，接受新的視角。這是等待和反思的時候。'},
    {"cardName":'吊人(The Hanged Man)逆位', "cardDes":'你可能會感到困擾或無法放下。試著調整心態，接受改變，找到新的解決方案。'},
    {"cardName":'死神(Death)正位', "cardDes":'今天是結束和轉變的時候。接受過去的結束，準備迎接新的開始。'},
    {"cardName":'死神(Death)逆位', "cardDes":'你可能會抗拒變化或固守舊有狀況。學會放下過去，迎接新的機會。'},
    {"cardName":'節制(Temperance)正位', "cardDes":'今天是尋找平衡和和諧的時候。保持冷靜，調整生活中的各種元素，達到內外平衡。'},
    {"cardName":'節制(Temperance)逆位', "cardDes":'你可能會感到失去平衡或過度。注意不要過度放縱或極端，尋找適當的中庸之道。'},
    {"cardName":'魔鬼(The Devil)正位', "cardDes":'今天可能會面臨誘惑或束縛。注意不要被負面情緒或習慣困住，尋求解脫和自由。'},
    {"cardName":'魔鬼(The Devil)逆位', "cardDes":'你可能正在努力擺脫束縛。繼續向前，克服負面的影響，尋找內心的解脫。'},
    {"cardName":'塔(The Tower)正位', "cardDes":'今天可能會有意外的變故或突破。接受變化，從困境中學習和成長。'},
    {"cardName":'塔(The Tower)逆位', "cardDes":'你可能會經歷內部的震蕩或衝突。試著保持冷靜，尋找重建和修復的機會。'},
    {"cardName":'星星(The Star)正位', "cardDes":'今天是充滿希望和靈感的時候。相信自己的夢想，保持正面積極，追求目標。'},
    {"cardName":'星星(The Star)逆位', "cardDes":'你可能會感到失望或缺乏信心。重新激發自己的希望，尋找新的靈感和動力。'},
    {"cardName":'月亮(The Moon)正位', "cardDes":'今天是探索內心和潛意識的好時機。注意夢境和直覺，它們會提供有價值的指引。'},
    {"cardName":'月亮(The Moon)逆位', "cardDes":'你可能會感到混亂或不安。試著理清思路，避免過度幻想，尋求真實的答案。'},
    {"cardName":'太陽(The Sun)正位', "cardDes":'今天充滿了活力和快樂。享受生活的美好，展示你的熱情和自信。'},
    {"cardName":'太陽(The Sun)逆位', "cardDes":'你可能會感到失去活力或遇到小障礙。保持積極的心態，尋找小的快樂和成功。'},
    {"cardName":'審判(Judgement)正位', "cardDes":'今天可能會迎來重生和覺醒。接受過去的教訓，展望未來，作出明智的選擇。'},
    {"cardName":'審判(Judgement)逆位', "cardDes":'你可能會感到自我評價不足或無法接受變化。面對內心的問題，尋找自我提升的途徑。'},
    {"cardName":'世界(The World)正位', "cardDes":'今天是達成目標和完成任務的時候。慶祝你的成就，準備迎接新的冒險。'},
    {"cardName":'世界(The World)逆位', "cardDes":'你可能會感到未完成或不滿。檢查是否有未解決的問題，並努力完成它們。'},
    {"cardName":'權杖一(The Ace of Wands)正位', "cardDes":'今天是充滿創造力和新機會的時候。抓住新的想法，勇敢地追求你的激情。'},
    {"cardName":'權杖一(The Ace of Wands)逆位', "cardDes":'你可能會感到創意阻塞或缺乏動力。尋找新的靈感，重新激發你的熱情。'},
    {"cardName":'權杖二(The Two of Wands)正位', "cardDes":'今天是制定計劃和展望未來的時候。做出明確的決定，為未來鋪路。'},
    {"cardName":'權杖二(The Two of Wands)逆位', "cardDes":'你可能會感到困惑或無法做出選擇。冷靜下來，重新評估你的選擇，尋找清晰的方向。'},
    {"cardName":'權杖三(The Three of Wands)正位', "cardDes":'今天是展望和等待成果的時候。你正在為未來的成功鋪路，耐心等待回報。'},
    {"cardName":'權杖三(The Three of Wands)逆位', "cardDes":'你可能會感到進展緩慢或遇到障礙。重新評估你的計劃，尋找改進的方式。'},
    {"cardName":'權杖四(The Four of Wands)正位', "cardDes":'今天是慶祝和享受成就的時候。與家人和朋友分享你的喜悅，感受穩定和和諧。'},
    {"cardName":'權杖四(The Four of Wands)逆位', "cardDes":'你可能會感到不穩定或面臨家庭問題。尋找解決問題的辦法，恢復平衡。'},
    {"cardName":'權杖五(The Five of Wands)正位', "cardDes":'今天可能會面臨挑戰或衝突。以積極的態度面對競爭，尋找解決方案。'},
    {"cardName":'權杖五(The Five of Wands)逆位', "cardDes":'你可能會感到衝突或緊張的緩解。保持冷靜，處理問題，尋求和平的解決辦法。'},
    {"cardName":'權杖六(The Six of Wands)正位', "cardDes":'今天是慶祝勝利和成功的時候。你將得到認可和讚賞，繼續保持積極。'},
    {"cardName":'權杖六(The Six of Wands)逆位', "cardDes":'你可能會感到缺乏認可或面臨挑戰。重新檢視你的目標，尋找支持和鼓勵。'},
    {"cardName":'權杖七(The Seven of Wands)正位', "cardDes":'今天是捍衛立場和克服障礙的時候。保持堅定，應對挑戰，展現你的勇氣。'},
    {"cardName":'權杖七(The Seven of Wands)逆位', "cardDes":'你可能會感到過度防守或焦慮。試著冷靜下來，尋找合適的解決方案，避免過度對抗。'},
    {"cardName":'權杖八(The Eight of Wands)正位', "cardDes":'今天可能會有迅速的進展或變化。保持靈活，抓住機會，快速行動。'},
    {"cardName":'權杖八(The Eight of Wands)逆位', "cardDes":'你可能會感到進展緩慢或受到阻礙。耐心等待，調整計劃，尋找前進的路徑。'},
    {"cardName":'權杖九(The Nine of Wands)正位', "cardDes":'今天是堅持和保持警惕的時候。面對挑戰時保持堅韌，準備應對最後的考驗。'},
    {"cardName":'權杖九(The Nine of Wands)逆位', "cardDes":'你可能會感到疲倦或不安。尋找放鬆和恢復的方式，避免過度壓力。'},
    {"cardName":'權杖十(The Ten of Wands)正位', "cardDes":'今天可能會感到負擔沉重。努力尋找平衡，考慮委派任務或尋求支持。'},
    {"cardName":'權杖十(The Ten of Wands)逆位', "cardDes":'你可能會感到壓力或責任過重。尋找釋放壓力的方法，保持身心健康。'},
    {"cardName":'權杖侍從(The Page of Wands)正位', "cardDes":'今天充滿了探索和創新的機會。勇敢地追求新的想法，展現你的創造力。'},
    {"cardName":'權杖侍從(The Page of Wands)逆位', "cardDes":'你可能會感到創意枯竭或不確定。尋找新的靈感，保持開放的心態。'},
    {"cardName":'權杖騎士(The Knight of Wands)正位', "cardDes":'今天你充滿了活力和冒險精神。勇敢地追求你的目標，克服挑戰。'},
    {"cardName":'權杖騎士(The Knight of Wands)逆位', "cardDes":'你可能會感到衝動或缺乏方向。調整你的行動計劃，尋找新的動力。'},
    {"cardName":'權杖女王(The Queen of Wands)正位', "cardDes":'今天你展現了領導力和魅力。利用你的能量和創造力，激勵他人，實現目標。'},
    {"cardName":'權杖女王(The Queen of Wands)逆位', "cardDes":'你可能會感到情緒不穩或缺乏信心。尋找內心的力量，恢復你的自信。'},
    {"cardName":'權杖國王(The King of Wands)正位', "cardDes":'今天你展現了強大的領導力和決策能力。積極行動，實現你的願景。'},
    {"cardName":'權杖國王(The King of Wands)逆位', "cardDes":'你可能會面臨權威或控制問題。檢查是否存在不合理的行為，尋求調整和改進。'},
    {"cardName":'聖杯一(The Ace of Cups)正位', "cardDes":'今天是情感充盈和新的關係的時候。打開心扉，接受愛和關懷。'},
    {"cardName":'聖杯一(The Ace of Cups)逆位', "cardDes":'你可能會感到情感封閉或不安。尋找釋放情感的方式，恢復內心的平衡。'},
    {"cardName":'聖杯二(The Two of Cups)正位', "cardDes":'今天是建立和諧關係和合作的好時機。珍惜與他人的連結，建立穩定的關係。'},
    {"cardName":'聖杯二(The Two of Cups)逆位', "cardDes":'你可能會面臨關係上的摩擦或不和。溝通和解決問題，尋找重新建立聯繫的途徑。'},
    {"cardName":'聖杯三(The Three of Cups)正位', "cardDes":'今天是慶祝和享受友情的時候。與朋友和家人共享快樂，建立深厚的情感聯繫。'},
    {"cardName":'聖杯三(The Three of Cups)逆位', "cardDes":'你可能會感到社交上的孤立或誤解。尋找合適的方式來建立連結和恢復關係。'},
    {"cardName":'聖杯四(The Four of Cups)正位', "cardDes":'今天你可能會感到情感上的不滿或疏離。重新評估你的需求，尋找新的機會。'},
    {"cardName":'聖杯四(The Four of Cups)逆位', "cardDes":'你可能會迎來新的機會和靈感。打開心扉，接受生活中的新體驗。'},
    {"cardName":'聖杯五(The Five of Cups)正位', "cardDes":'今天可能會感到失落或悲傷。接受過去的情感，尋找康復和前進的道路。'},
    {"cardName":'聖杯五(The Five of Cups)逆位', "cardDes":'你可能會開始恢復和尋找希望。逐步放下過去的悲傷，迎接未來的機會。'},
    {"cardName":'聖杯六(The Six of Cups)正位', "cardDes":'今天是回憶和重拾美好時光的時候。珍惜過去的經驗，帶來溫暖和快樂。'},
    {"cardName":'聖杯六(The Six of Cups)逆位', "cardDes":'你可能會感到對過去的懷念或困擾。尋找釋放情感的方式，專注於當下的生活。'},
    {"cardName":'聖杯七(The Seven of Cups)正位', "cardDes":'今天可能會面臨許多選擇和幻想。冷靜分析每個選擇，避免被誘惑所困。'},
    {"cardName":'聖杯七(The Seven of Cups)逆位', "cardDes":'你可能會開始清晰地看待現實。整理你的選擇，做出明智的決策。'},
    {"cardName":'聖杯八(The Eight of Cups)正位', "cardDes":'今天是放下過去和尋求新的方向的時候。勇敢地離開舒適區，追求更高的目標。'},
    {"cardName":'聖杯八(The Eight of Cups)逆位', "cardDes":'你可能會感到困於現狀或難以放手。尋找改變的勇氣，釋放過去的束縛。'},
    {"cardName":'聖杯九(The Nine of Cups)正位', "cardDes":'今天是滿足和實現願望的時候。享受你所擁有的幸福，珍惜生活的美好。'},
    {"cardName":'聖杯九(The Nine of Cups)逆位', "cardDes":'你可能會感到不滿足或缺乏喜悅。檢查內心的需求，尋找新的滿足感。'},
    {"cardName":'聖杯十(The Ten of Cups)正位', "cardDes":'今天充滿了家庭和諧與幸福。珍惜和家人共享的美好時光，感受生活的充實。'},
    {"cardName":'聖杯十(The Ten of Cups)逆位', "cardDes":'你可能會感到家庭或關係上的困難。尋找解決方案，努力恢復和諧。'},
    {"cardName":'聖杯侍從(The Page of Cups)正位', "cardDes":'今天是感受情感和直覺的好時機。開放心扉，接受新的靈感和情感體驗。'},
    {"cardName":'聖杯侍從(The Page of Cups)逆位', "cardDes":'你可能會感到情感困擾或不安。尋找支持，恢復內心的平衡。'},
    {"cardName":'聖杯騎士(The Knight of Cups)正位', "cardDes":'今天充滿了浪漫和情感的機會。追隨你的心，展現愛意和關懷。'},
    {"cardName":'聖杯騎士(The Knight of Cups)逆位', "cardDes":'你可能會感到情感上的困擾或不穩定。試著理清情感，避免過度理想化。'},
    {"cardName":'聖杯女王(The Queen of Cups)正位', "cardDes":'今天你展現了深厚的同情心和直覺。善待自己和他人，感受情感的流動。'},
    {"cardName":'聖杯女王(The Queen of Cups)逆位', "cardDes":'你可能會感到情感封閉或焦慮。尋找釋放情感的方式，恢復內心的平衡。'},
    {"cardName":'聖杯國王(The King of Cups)正位', "cardDes":'今天你展現了情感的成熟和智慧。利用你的洞察力和同情心，處理情感上的問題。'},
    {"cardName":'聖杯國王(The King of Cups)逆位', "cardDes":'你可能會感到情感上的混亂或不穩定。努力平衡你的情感，尋找解決困難的方法。'},
    {"cardName":'寶劍一(The Ace of Swords)正位', "cardDes":'今天是啟迪智慧和清晰思維的時候。使用你的直覺和智慧，解決問題，做出明確的決策。'},
    {"cardName":'寶劍一(The Ace of Swords)逆位', "cardDes":'你可能會面臨困難的決定或思維混亂。嘗試冷靜下來，尋找清晰的解決方案。'},
    {"cardName":'寶劍二(The Two of Swords)正位', "cardDes":'今天是面對選擇和決策的時候。平衡各方觀點，做出理智的決定。'},
    {"cardName":'寶劍二(The Two of Swords)逆位', "cardDes":'你可能會感到困擾或難以做出選擇。嘗試打開心扉，尋找解決問題的辦法。'},
    {"cardName":'寶劍三(The Three of Swords)正位', "cardDes":'今天可能會面臨心痛或情感上的困擾。接受傷痛，尋找治癒的方法。'},
    {"cardName":'寶劍三(The Three of Swords)逆位', "cardDes":'你可能會開始恢復和釋放過去的痛苦。尋找內心的平靜，修復受損的情感。'},
    {"cardName":'寶劍四(The Four of Swords)正位', "cardDes":'今天是休息和恢復的時候。給自己一些放鬆的時間，整理思緒，重獲精力。'},
    {"cardName":'寶劍四(The Four of Swords)逆位', "cardDes":'你可能會感到焦慮或無法放鬆。試著尋找安靜的時間，恢復內心的平靜。'},
    {"cardName":'寶劍五(The Five of Swords)正位', "cardDes":'今天可能會面臨衝突或爭執。保持冷靜，尋找和平的解決方案，避免不必要的爭端。'},
    {"cardName":'寶劍五(The Five of Swords)逆位', "cardDes":'你可能會經歷沖突的平息或解決。尋找和解的機會，恢復關係的和諧。'},
    {"cardName":'寶劍六(The Six of Swords)正位', "cardDes":'今天是過渡和前進的時候。離開過去的困境，迎接新的環境和機會。'},
    {"cardName":'寶劍六(The Six of Swords)逆位', "cardDes":'你可能會感到過渡過程中的困難。尋找支持，逐步克服障礙，向前邁進。'},
    {"cardName":'寶劍七(The Seven of Swords)正位', "cardDes":'今天可能會面臨需要謀略和策略的情況。注意不要被欺騙，保持誠實和警覺。'},
    {"cardName":'寶劍七(The Seven of Swords)逆位', "cardDes":'你可能會面臨揭露和暴露。檢查你的行為，尋求真相和清晰度。'},
    {"cardName":'寶劍八(The Eight of Swords)正位', "cardDes":'今天可能會感到困境或束縛。尋找解決方案，尋求支持，重新獲得自由。'},
    {"cardName":'寶劍八(The Eight of Swords)逆位', "cardDes":'你可能會開始擺脫困境或限制。努力克服挑戰，尋找新的可能性。'},
    {"cardName":'寶劍九(The Nine of Swords)正位', "cardDes":'今天可能會面臨焦慮或擔憂。嘗試放鬆心情，尋找解決方法，減少壓力。'},
    {"cardName":'寶劍九(The Nine of Swords)逆位', "cardDes":'你可能會開始放下擔憂或焦慮。尋找支持，恢復內心的平靜。'},
    {"cardName":'寶劍十(The Ten of Swords)正位', "cardDes":'今天可能會經歷結束或重大的困難。接受結束，尋找重生的機會。'},
    {"cardName":'寶劍十(The Ten of Swords)逆位', "cardDes":'你可能會面臨困境的緩解。尋找新的開始，走出過去的陰影。'},
    {"cardName":'寶劍侍從(The Page of Swords)正位', "cardDes":'今天充滿了智慧和觀察力的機會。保持警覺，尋找真相，勇敢面對挑戰。'},
    {"cardName":'寶劍侍從(The Page of Swords)逆位', "cardDes":'你可能會感到思維混亂或缺乏方向。尋找清晰的思路，保持冷靜。'},
    {"cardName":'寶劍騎士(The Knight of Swords)正位', "cardDes":'今天充滿了迅速行動和決策的機會。勇敢地追求目標，克服挑戰。'},
    {"cardName":'寶劍騎士(The Knight of Swords)逆位', "cardDes":'你可能會感到衝動或缺乏計劃。重新評估你的行動，尋找理智的決策。'},
    {"cardName":'寶劍女王(The Queen of Swords)正位', "cardDes":'今天你展現了智慧和清晰的思維。利用你的洞察力和分析能力，處理問題和挑戰。'},
    {"cardName":'寶劍女王(The Queen of Swords)逆位', "cardDes":'你可能會感到情感上的困擾或理智上的混亂。尋找內心的平衡，避免過度理性化。'},
    {"cardName":'寶劍國王(The King of Swords)正位', "cardDes":'今天展現了強大的智慧和決策能力。以公平和理智的方式處理問題，保持清晰的思路。'},
    {"cardName":'寶劍國王(The King of Swords)逆位', "cardDes":'你可能會面臨決策上的困難或不公正的情況。尋求平衡和公正，避免過度控制。'},
    {"cardName":'錢幣一(The Ace of Pentacles)正位', "cardDes":'今天是實現財務和物質成功的好時機。抓住新的機會，投資未來。'},
    {"cardName":'錢幣一(The Ace of Pentacles)逆位', "cardDes":'你可能會感到財務上的困難或不穩定。檢查你的財務計劃，尋找穩定的策略。'},
    {"cardName":'錢幣二(The Two of Pentacles)正位', "cardDes":'今天是平衡和管理多重任務的時候。合理安排時間，保持穩定和靈活。'},
    {"cardName":'錢幣二(The Two of Pentacles)逆位', "cardDes":'你可能會感到壓力過大或難以平衡。尋找有效的管理方式，減少壓力。'},
    {"cardName":'錢幣三(The Three of Pentacles)正位', "cardDes":'今天是團隊合作和實現目標的好時機。與他人協作，展示你的專業技能。'},
    {"cardName":'錢幣三(The Three of Pentacles)逆位', "cardDes":'你可能會面臨合作上的挑戰或困難。尋找改善合作的方式，保持溝通。'},
    {"cardName":'錢幣四(The Four of Pentacles)正位', "cardDes":'今天是穩定和保護財務的時候。檢查你的財務狀況，保持財務的安全和穩定。'},
    {"cardName":'錢幣四(The Four of Pentacles)逆位', "cardDes":'你可能會感到財務上的不穩定或焦慮。尋找平衡和安全的財務管理方式。'},
    {"cardName":'錢幣五(The Five of Pentacles)正位', "cardDes":'今天可能會面臨財務困難或缺乏安全感。尋找支持，檢查財務狀況，努力克服困難。'},
    {"cardName":'錢幣五(The Five of Pentacles)逆位', "cardDes":'你可能會開始恢復財務上的穩定。尋找積極的解決方案，重建財務安全。'},
    {"cardName":'錢幣六(The Six of Pentacles)正位', "cardDes":'今天是施予和接受幫助的好時機。分享你的資源，尋求支持和回報。'},
    {"cardName":'錢幣六(The Six of Pentacles)逆位', "cardDes":'你可能會感到財務上的不平衡。檢查資源的分配，尋找公平和穩定的方式。'},
    {"cardName":'錢幣七(The Seven of Pentacles)正位', "cardDes":'今天是檢視和評估成果的時候。耐心等待，觀察你的努力所帶來的回報。'},
    {"cardName":'錢幣七(The Seven of Pentacles)逆位', "cardDes":'你可能會感到成果不如預期。檢查你的計劃，尋找改進的途徑。'},
    {"cardName":'錢幣八(The Eight of Pentacles)正位', "cardDes":'今天是努力和提升技能的時候。專注於工作，持續進步，提升你的專業能力。'},
    {"cardName":'錢幣八(The Eight of Pentacles)逆位', "cardDes":'你可能會感到工作上的倦怠或缺乏動力。尋找激勵的方法，重拾工作的熱情。'},
    {"cardName":'錢幣九(The Nine of Pentacles)正位', "cardDes":'今天充滿了成功和滿足。享受你所擁有的物質成就，感受生活的豐盛。'},
    {"cardName":'錢幣九(The Nine of Pentacles)逆位', "cardDes":'你可能會感到不滿足或缺乏安全感。檢查你的需求，尋找滿足的方式。'},
    {"cardName":'錢幣十(The Ten of Pentacles)正位', "cardDes":'今天是家庭和物質成功的時候。珍惜與家人的連結，享受長期的穩定和成就。'},
    {"cardName":'錢幣十(The Ten of Pentacles)逆位', "cardDes":'你可能會面臨家庭或財務上的挑戰。尋找解決方案，恢復穩定和安全。'},
    {"cardName":'錢幣侍從(The Page of Pentacles)正位', "cardDes":'今天充滿了學習和成長的機會。抓住新的挑戰，提升你的技能和知識。'},
    {"cardName":'錢幣侍從(The Page of Pentacles)逆位', "cardDes":'你可能會感到學習上的困難或缺乏進展。尋找新的方法，保持努力。'},
    {"cardName":'錢幣騎士(The Knight of Pentacles)正位', "cardDes":'今天是穩定和踏實工作的時候。專注於目標，保持耐心，穩步前進。'},
    {"cardName":'錢幣騎士(The Knight of Pentacles)逆位', "cardDes":'你可能會感到工作上的停滯或倦怠。尋找新的動力，重新激發工作的熱情。'},
    {"cardName":'錢幣女王(The Queen of Pentacles)正位', "cardDes":'今天展現了關懷和實用的能力。關注家庭和財務，保持實用的態度。'},
    {"cardName":'錢幣女王(The Queen of Pentacles)逆位', "cardDes":'你可能會感到家庭或財務上的壓力。尋找平衡，恢復安定和和諧。'},
    {"cardName":'錢幣國王(The King of Pentacles)正位', "cardDes":'今天展現了成熟和財務上的智慧。利用你的經驗和資源，實現長期的成功。'},
    {"cardName":'錢幣國王(The King of Pentacles)逆位', "cardDes":'你可能會面臨財務上的挑戰或過度控制。尋找平衡，保持實用的態度。'},
    {"cardName":'隱士(The Hermit)正位', "cardDes":'今天是內省和尋找智慧的時候。給自己一些獨處的時間，探索內心的真實。'},
    {"cardName":'隱士(The Hermit)逆位', "cardDes":'你可能會感到孤立或難以尋找指引。尋找外界的支持，與他人分享你的感受。'},
    {"cardName":'命運之輪(The Wheel of Fortune)正位', "cardDes":'今天充滿了變化和機會。接受生命中的轉折，利用機會實現你的目標。'},
    {"cardName":'命運之輪(The Wheel of Fortune)逆位', "cardDes":'你可能會面臨挑戰或變化的困難。尋找穩定的支持，保持靈活應對變化。'},
    {"cardName":'力量(The Strength)正位', "cardDes":'今天展現了你的內在力量和勇氣。面對挑戰，保持堅定和自信。'},
    {"cardName":'力量(The Strength)逆位', "cardDes":'你可能會感到缺乏力量或自信。尋找支持，恢復你的內在力量和勇氣。'},
    {"cardName":'吊人(The Hanged Man)正位', "cardDes":'今天是放下過去和接受改變的時候。從不同的角度看待問題，尋求新的觀點。'},
    {"cardName":'吊人(The Hanged Man)逆位', "cardDes":'你可能會感到困擾或難以接受改變。尋找釋放壓力的方式，保持靈活應對。'},
    {"cardName":'死神(The Death)正位', "cardDes":'今天可能會經歷重大的變化或結束。接受變化，尋找新的開始和機會。'},
    {"cardName":'死神(The Death)逆位', "cardDes":'你可能會面臨變化的抵抗或困難。尋找釋放和調整的方式，迎接新的可能性。'},
    {"cardName":'節制(The Temperance)正位', "cardDes":'今天是平衡和調和的時候。尋求內心的平靜，平衡各方面的需求。'},
    {"cardName":'節制(The Temperance)逆位', "cardDes":'你可能會感到失衡或過度。尋找恢復平衡的方法，避免過度行為。'},
    {"cardName":'惡魔(The Devil)正位', "cardDes":'今天可能會面臨誘惑或困擾。警惕負面的影響，尋求解脫和自由。'},
    {"cardName":'惡魔(The Devil)逆位', "cardDes":'你可能會擺脫束縛或克服困難。尋找新的開始，恢復自由和清晰。'},
    {"cardName":'塔(The Tower)正位', "cardDes":'今天可能會經歷突如其來的變化或破壞。接受變化，尋找重建的機會。'},
    {"cardName":'塔(The Tower)逆位', "cardDes":'你可能會面臨緩慢的變化或困難。尋找穩定的支持，逐步克服挑戰。'},
    {"cardName":'星星(The Star)正位', "cardDes":'今天充滿了希望和靈感。接受積極的能量，尋找實現目標的機會。'},
    {"cardName":'星星(The Star)逆位', "cardDes":'你可能會感到失望或缺乏信心。尋找內在的希望，恢復對未來的信念。'},
    {"cardName":'月亮(The Moon)正位', "cardDes":'今天可能會面臨不確定性或隱藏的真相。保持警覺，探索內心的直覺。'},
    {"cardName":'月亮(The Moon)逆位', "cardDes":'你可能會開始看清事物的真相。尋找清晰的指引，擺脫不確定性。'},
    {"cardName":'太陽(The Sun)正位', "cardDes":'今天充滿了快樂和成功。享受生活的美好，分享你的幸福。'},
    {"cardName":'太陽(The Sun)逆位', "cardDes":'你可能會感到失落或缺乏光明。尋找內心的陽光，恢復積極的能量。'},
    {"cardName":'審判(The Judgment)正位', "cardDes":'今天是自我反省和重生的時候。接受過去的經驗，尋找新的方向和成長。'},
    {"cardName":'審判(The Judgment)逆位', "cardDes":'你可能會面臨自我批評或過度反思。尋找放下過去的方法，專注於當下的成長。'},
    {"cardName":'世界(The World)正位', "cardDes":'今天充滿了完成和成就。慶祝你的成功，接受新的開始和機會。'},
    {"cardName":'世界(The World)逆位', "cardDes":'你可能會感到未完成或挑戰。尋找完成的方式，努力克服障礙。'}
]

work = [
    {"cardName": '愚者(The Fool)正位', "cardDes": '今天你可能會遇到新的機會或挑戰，保持開放的心態和勇氣來接受未知的事物。敢於冒險可能會帶來意想不到的成功。'},
    {"cardName": '愚者(The Fool)逆位', "cardDes": '今天要小心過於冒失或輕率的行為。計劃和準備是關鍵，不要輕易做出決定或開始新項目。'},
    {"cardName": '魔術師(The Magician)正位', "cardDes": '今天是發揮你技能和才能的好時機。利用你的資源和能力來實現目標，並且自信地展示你的才華。'},
    {"cardName": '魔術師(The Magician)逆位', "cardDes": '今天可能會遇到挑戰，需要重新評估你的策略或技能。小心操控不當，避免欺騙或不誠實的行為。'},
    {"cardName": '女教皇(The High Priestess)正位', "cardDes": '今天適合靜下心來，聽從內心的聲音。相信你的直覺，並且不要急於求成，靜待答案的出現。'},
    {"cardName": '女教皇(The High Priestess)逆位', "cardDes": '今天可能會感到內心混亂或不安。試著放鬆，避免強迫自己做出決定。重新調整你的直覺和內在聲音。'},
    {"cardName": '皇后(The Empress)正位', "cardDes": '今天適合關注你的創意和生產力。善待自己和他人，關注生活中的美好事物，並且可能會迎來繁榮。'},
    {"cardName": '皇后(The Empress)逆位', "cardDes": '今天可能會面臨情感上的困難或創意的障礙。試著找到平衡，關注自我照顧和情感需求。'},
    {"cardName": '皇帝(The Emperor)正位', "cardDes": '今天適合展現你的領導能力和控制力。穩定的計劃和有力的決策能夠帶來成功。保持專注和紀律。'},
    {"cardName": '皇帝(The Emperor)逆位', "cardDes": '今天可能會面臨權威挑戰或管理上的困難。試著避免過度控制，並且重新評估你的策略。'},
    {"cardName": '教宗(The Hierophant)正位', "cardDes": '今天是尋求指導和學習的好時機。遵循傳統或尋找智慧的指導，並且保持謙遜的態度。'},
    {"cardName": '教宗(The Hierophant)逆位', "cardDes": '今天可能會遇到反叛或挑戰傳統的情況。試著開放思維，尋找自己的道路，而不是僅僅遵循既定規則。'},
    {"cardName": '戀人(The Lovers)正位', "cardDes": '今天適合做出重要的決定，特別是在關係或合作方面。保持誠實和透明，並且相信你的內心選擇。'},
    {"cardName": '戀人(The Lovers)逆位', "cardDes": '今天可能會面臨關係上的挑戰或選擇上的困難。重新評估你的選擇，尋找內心的平衡。'},
    {"cardName": '戰車(The Chariot)正位', "cardDes": '今天適合展現你的意志力和決心。通過積極的行動和掌握方向，你可以克服障礙並實現目標。'},
    {"cardName": '戰車(The Chariot)逆位', "cardDes": '今天可能會面臨困難或失去控制的情況。重新調整你的策略，避免衝動行事。'},
    {"cardName": '力量(The Strength)正位', "cardDes": '今天你可能需要展現內在的力量和勇氣。相信自己，並且用耐心和同情心來面對挑戰。'},
    {"cardName": '力量(The Strength)逆位', "cardDes": '今天可能會感到缺乏力量或面臨內在的掙扎。試著尋找支持，並且保持冷靜。'},
    {"cardName": '隱士(The Hermit)正位', "cardDes": '今天適合靜下心來，進行自我反思或尋求智慧。獨處的時刻可以幫助你找到答案和方向。'},
    {"cardName": '隱士(The Hermit)逆位', "cardDes": '今天可能會感到孤獨或迷失。試著尋找與他人的聯繫，並且不要過度隱藏自己的感受。'},
    {"cardName": '命運之輪(The Wheel of Fortune)正位', "cardDes": '今天是迎接變化和機遇的好時機。接受命運的變遷，並且保持靈活和開放的心態。'},
    {"cardName": '命運之輪(The Wheel of Fortune)逆位', "cardDes": '今天可能會感到變化的壓力或困難。試著保持耐心，並且尋找積極應對的方式。'},
    {"cardName": '正義(The Justice)正位', "cardDes": '今天適合做出公平和明智的決策。關注道德和法律問題，保持公正和誠實。'},
    {"cardName": '正義(The Justice)逆位', "cardDes": '今天可能會遇到不公平或誤解的情況。試著重新評估你的行為，並且尋找解決方案。'},
    {"cardName": '吊人(The Hanged Man)正位', "cardDes": '今天適合重新評估你的觀點和策略。放慢腳步，接受暫時的停滯，並且尋找新的洞察。'},
    {"cardName": '吊人(The Hanged Man)逆位', "cardDes": '今天可能會感到受阻或困於現狀。試著改變你的觀點，並且尋找突破困境的方法。'},
    {"cardName": '死神(The Death)正位', "cardDes": '今天是結束和轉變的時期。接受變化，讓過去的事物結束，並且準備迎接新的開始。'},
    {"cardName": '死神(The Death)逆位', "cardDes": '今天可能會面臨抵抗變化或結束的困難。試著接受改變，並且放下過去的事物。'},
    {"cardName": '節制(The Temperance)正位', "cardDes": '今天適合尋求平衡和和諧。通過調整和妥協，你可以達到理想的狀態。'},
    {"cardName": '節制(The Temperance)逆位', "cardDes": '今天可能會感到不平衡或過度。試著找到中庸之道，避免過度行為。'},
    {"cardName": '魔鬼(The Devil)正位', "cardDes": '今天可能會面臨誘惑或困境。警惕過度依賴或被束縛，努力尋找自由和解脫。'},
    {"cardName": '魔鬼(The Devil)逆位', "cardDes": '今天可能會開始擺脫束縛或負面影響。尋找自我解放和改善的方法。'},
    {"cardName": '塔(The Tower)正位', "cardDes": '今天可能會經歷突然的變化或挑戰。這些變化雖然劇烈，但可能會帶來必要的突破。'},
    {"cardName": '塔(The Tower)逆位', "cardDes": '今天可能會感到困境加劇或難以適應變化。試著接受變化，並且找到穩定的支持。'},
    {"cardName": '星(The Star)正位', "cardDes": '今天是希望和靈感的時刻。保持積極的心態，尋找新的機會，並且相信未來會更好。'},
    {"cardName": '星(The Star)逆位', "cardDes": '今天可能會感到失望或缺乏信心。試著找到內在的希望，並且尋求支持和指導。'},
    {"cardName": '月(The Moon)正位', "cardDes": '今天適合關注潛意識和直覺。可能會遇到不確定性或混亂，但保持冷靜可以幫助你找到真相。'},
    {"cardName": '月(The Moon)逆位', "cardDes": '今天可能會感到迷失或混淆。試著理清思緒，並且避免過度依賴直覺。'},
    {"cardName": '太陽(The Sun)正位', "cardDes": '今天是享受成功和快樂的時刻。充滿積極能量，並且與他人分享你的喜悅。'},
    {"cardName": '太陽(The Sun)逆位', "cardDes": '今天可能會感到陰鬱或缺乏活力。試著找到小小的快樂，並且尋求積極的支持。'},
    {"cardName": '審判(The Judgment)正位', "cardDes": '今天適合反思和做出改變。接受過去的經歷，並且準備迎接新的階段。'},
    {"cardName": '審判(The Judgment)逆位', "cardDes": '今天可能會面臨內心的掙扎或不願接受變化。試著接受自我反省，並且找到解決的方法。'},
    {"cardName": '世界(The World)正位', "cardDes": '今天是完成和成就的時刻。感受你的成功，並且準備迎接新的挑戰。'},
    {"cardName": '世界(The World)逆位', "cardDes": '今天可能會感到困難或無法完成目標。試著尋找解決方案，並且保持堅定。'},
    {"cardName": '權杖一(The Ace of Wands)正位', "cardDes": '今天是展現創意和啟動新計劃的好時機。保持熱情，並且勇敢追求你的目標。'},
    {"cardName": '權杖一(The Ace of Wands)逆位', "cardDes": '今天可能會面臨創意阻塞或缺乏動力。試著找到激勵自己的方式，並且重新調整計劃。'},
    {"cardName": '權杖二(The Two of Wands)正位', "cardDes": '今天適合計劃和探索新的機會。保持開放的心態，並且做好長期規劃。'},
    {"cardName": '權杖二(The Two of Wands)逆位', "cardDes": '今天可能會感到猶豫或不確定。試著重新評估你的選擇，並且避免過度擔憂。'},
    {"cardName": '權杖三(The Three of Wands)正位', "cardDes": '今天適合展望未來和追求長期目標。保持積極，並且準備迎接即將到來的機會。'},
    {"cardName": '權杖三(The Three of Wands)逆位', "cardDes": '今天可能會感到進展緩慢或遇到困難。試著保持耐心，並且重新調整你的策略。'},
    {"cardName": '權杖四(The Four of Wands)正位', "cardDes": '今天是慶祝和建立穩定基礎的好時機。享受和他人的聯繫，並且關注你的成就。'},
    {"cardName": '權杖四(The Four of Wands)逆位', "cardDes": '今天可能會面臨家庭或社交問題。試著尋找解決方案，並且建立良好的溝通。'},
    {"cardName": '權杖五(The Five of Wands)正位', "cardDes": '今天可能會面臨競爭或衝突。保持冷靜，並且用積極的方式應對挑戰。'},
    {"cardName": '權杖五(The Five of Wands)逆位', "cardDes": '今天可能會感到競爭激烈或內部衝突。試著尋找和解的方法，並且避免無謂的爭論。'},
    {"cardName": '權杖六(The Six of Wands)正位', "cardDes": '今天是慶祝成功和獲得認可的時刻。自信地展示你的成就，並且享受你所取得的勝利。'},
    {"cardName": '權杖六(The Six of Wands)逆位', "cardDes": '今天可能會感到缺乏認可或支持。試著保持信心，並且專注於自己的目標。'},
    {"cardName": '權杖七(The Seven of Wands)正位', "cardDes": '今天是捍衛你的立場和應對挑戰的時候。保持堅定和勇敢，並且不懼困難。'},
    {"cardName": '權杖七(The Seven of Wands)逆位', "cardDes": '今天可能會感到被壓力或挑戰困擾。試著尋找支持，並且不要過於防衛。'},
    {"cardName": '權杖八(The Eight of Wands)正位', "cardDes": '今天適合快速行動和推進計劃。事情會迅速發展，保持積極並且迅速做出決策。'},
    {"cardName": '權杖八(The Eight of Wands)逆位', "cardDes": '今天可能會面臨延遲或進展緩慢。試著保持耐心，並且調整你的計劃。'},
    {"cardName": '權杖九(The Nine of Wands)正位', "cardDes": '今天適合面對困難並且保持堅持。你可能會感到疲憊，但你的努力將會得到回報。'},
    {"cardName": '權杖九(The Nine of Wands)逆位', "cardDes": '今天可能會感到身心疲憊或缺乏支持。試著尋找放鬆的方式，並且尋求幫助。'},
    {"cardName": '權杖十(The Ten of Wands)正位', "cardDes": '今天可能會感到壓力或負擔加重。試著尋找分擔的方法，並且有效地管理你的工作。'},
    {"cardName": '權杖十(The Ten of Wands)逆位', "cardDes": '今天可能會感到過度負擔或不堪重負。試著重新評估你的責任，並且尋找放鬆的方法。'},
    {"cardName": '權杖侍者(The Page of Wands)正位', "cardDes": '今天適合展現創意和探索新的機會。保持好奇心，並且勇敢地追求你的興趣。'},
    {"cardName": '權杖侍者(The Page of Wands)逆位', "cardDes": '今天可能會感到缺乏動力或方向。試著重新尋找你的興趣，並且避免過度衝動。'},
    {"cardName": '權杖騎士(The Knight of Wands)正位', "cardDes": '今天適合展現你的活力和冒險精神。積極行動，並且勇敢追求新的挑戰。'},
    {"cardName": '權杖騎士(The Knight of Wands)逆位', "cardDes": '今天可能會面臨衝動或計劃不周的困難。試著保持冷靜，並且仔細評估你的計劃。'},
    {"cardName": '權杖女王(The Queen of Wands)正位', "cardDes": '今天是展現你魅力和創意的時刻。充滿自信地面對挑戰，並且用你的熱情感染他人。'},
    {"cardName": '權杖女王(The Queen of Wands)逆位', "cardDes": '今天可能會感到缺乏自信或遇到情緒困擾。試著尋找支持，並且重新調整你的目標。'},
    {"cardName": '權杖國王(The King of Wands)正位', "cardDes": '今天適合展現領導力和遠見。用你的策略和決策能力來推動你的計劃。'},
    {"cardName": '權杖國王(The King of Wands)逆位', "cardDes": '今天可能會面臨領導上的挑戰或沖突。試著保持冷靜，並且尋找合作的方式。'},
    {"cardName": '聖杯一(The Ace of Cups)正位', "cardDes": '今天是開始新的情感關係或創造性工作的好時機。接受愛與靈感，並且保持開放的心態。'},
    {"cardName": '聖杯一(The Ace of Cups)逆位', "cardDes": '今天可能會感到情感上的困難或空虛。試著關注自我照顧，並且尋找情感上的支持。'},
    {"cardName": '聖杯二(The Two of Cups)正位', "cardDes": '今天適合建立和加強關係。尋找和諧與合作，並且享受你與他人的聯繫。'},
    {"cardName": '聖杯二(The Two of Cups)逆位', "cardDes": '今天可能會面臨關係上的問題或不和諧。試著解決衝突，並且尋找和解的方法。'},
    {"cardName": '聖杯三(The Three of Cups)正位', "cardDes": '今天是慶祝和分享的時刻。與朋友和家人聚會，享受社交活動和喜悅。'},
    {"cardName": '聖杯三(The Three of Cups)逆位', "cardDes": '今天可能會感到社交壓力或孤獨。試著尋找與他人聯繫的機會，並且避免過度依賴外界認可。'},
    {"cardName": '聖杯四(The Four of Cups)正位', "cardDes": '今天可能會感到情感上的不滿或困惑。重新評估你的需求，並且尋找新的機會來激發興趣。'},
    {"cardName": '聖杯四(The Four of Cups)逆位', "cardDes": '今天可能會開始重新興趣和情感上的突破。試著打開心扉，接受新的可能性。'},
    {"cardName": '聖杯五(The Five of Cups)正位', "cardDes": '今天可能會面臨失落或悲傷。試著接受情感上的挑戰，並且尋找重新振作的力量。'},
    {"cardName": '聖杯五(The Five of Cups)逆位', "cardDes": '今天可能會感到開始從失落中恢復。尋找積極的解決方案，並且感激你所擁有的。'},
    {"cardName": '聖杯六(The Six of Cups)正位', "cardDes": '今天是回憶和重溫美好時光的好時機。尋找過去的靈感，並且與親朋好友聯繫。'},
    {"cardName": '聖杯六(The Six of Cups)逆位', "cardDes": '今天可能會面臨對過去的困惑或情感上的問題。試著接受當前的情況，並且尋找前進的方式。'},
    {"cardName": '聖杯七(The Seven of Cups)正位', "cardDes": '今天適合探索不同的選擇和機會。保持開放的心態，並且謹慎地做出決策。'},
    {"cardName": '聖杯七(The Seven of Cups)逆位', "cardDes": '今天可能會感到困惑或面臨選擇上的障礙。重新評估你的選擇，並且避免過度理想化。'},
    {"cardName": '聖杯八(The Eight of Cups)正位', "cardDes": '今天是離開過去的困境和尋找新機會的時刻。勇敢地放下過去，並且追求新的方向。'},
    {"cardName": '聖杯八(The Eight of Cups)逆位', "cardDes": '今天可能會感到難以放下過去的事物。試著重新評估你的情感需求，並且尋找支持。'},
    {"cardName": '聖杯九(The Nine of Cups)正位', "cardDes": '今天是滿足和幸福的時刻。享受你的成就和滿足感，並且感激生活中的美好事物。'},
    {"cardName": '聖杯九(The Nine of Cups)逆位', "cardDes": '今天可能會感到不滿或缺乏滿足感。試著找到真正的需求，並且調整你的期望。'},
    {"cardName": '聖杯十(The Ten of Cups)正位', "cardDes": '今天是家庭和情感幸福的好時機。與家人和朋友分享你的喜悅，並且感受圓滿。'},
    {"cardName": '聖杯十(The Ten of Cups)逆位', "cardDes": '今天可能會面臨家庭或情感上的挑戰。試著尋找解決方案，並且關注關係中的和諧。'},
    {"cardName": '聖杯侍者(The Page of Cups)正位', "cardDes": '今天適合展現你的情感和創意。保持開放的心態，並且接受新的情感體驗。'},
    {"cardName": '聖杯侍者(The Page of Cups)逆位', "cardDes": '今天可能會感到情感上的困惑或不安。試著尋找支持，並且保持自我照顧。'},
    {"cardName": '聖杯騎士(The Knight of Cups)正位', "cardDes": '今天是追求情感和浪漫的時刻。保持敏感和誠實，並且勇敢表達你的感受。'},
    {"cardName": '聖杯騎士(The Knight of Cups)逆位', "cardDes": '今天可能會面臨情感上的困難或迷茫。試著尋找真實的情感連結，並且避免逃避現實。'},
    {"cardName": '聖杯女王(The Queen of Cups)正位', "cardDes": '今天適合關注你的情感和直覺。保持關懷和同情心，並且關注他人的需求。'},
    {"cardName": '聖杯女王(The Queen of Cups)逆位', "cardDes": '今天可能會面臨情感上的困境或過度敏感。試著尋找內心的平靜，並且避免過度依賴他人。'},
    {"cardName": '聖杯國王(The King of Cups)正位', "cardDes": '今天適合展現你的情感智慧和穩定。保持冷靜和理解，並且在關係中發揮領導作用。'},
    {"cardName": '聖杯國王(The King of Cups)逆位', "cardDes": '今天可能會感到情感上的挑戰或缺乏控制。試著找到內在的平衡，並且避免情感上的衝突。'},
    {"cardName": '寶劍一(The Ace of Swords)正位', "cardDes": '今天是獲得清晰和真理的時刻。用理智和分析來解決問題，並且勇敢地面對挑戰。'},
    {"cardName": '寶劍一(The Ace of Swords)逆位', "cardDes": '今天可能會面臨思維上的困惑或錯誤的判斷。試著重新評估你的觀點，並且尋求真相。'},
    {"cardName": '寶劍二(The Two of Swords)正位', "cardDes": '今天適合做出平衡的決策。保持冷靜，並且避免衝動行事。尋找內心的平衡。'},
    {"cardName": '寶劍二(The Two of Swords)逆位', "cardDes": '今天可能會感到選擇困難或內心衝突。試著清理思緒，並且尋找明確的解決方案。'},
    {"cardName": '寶劍三(The Three of Swords)正位', "cardDes": '今天可能會面臨情感上的傷害或困難。接受你的感受，並且尋找治癒和支持。'},
    {"cardName": '寶劍三(The Three of Swords)逆位', "cardDes": '今天可能會感到情感上的恢復或釋放。試著尋找和解的方式，並且關注情感的修復。'},
    {"cardName": '寶劍四(The Four of Swords)正位', "cardDes": '今天適合休息和恢復。給自己時間放鬆，並且重新充電。保持靜心和沉思。'},
    {"cardName": '寶劍四(The Four of Swords)逆位', "cardDes": '今天可能會感到壓力或需要調整休息的方式。試著尋找放鬆的機會，並且避免過度疲勞。'},
    {"cardName": '寶劍五(The Five of Swords)正位', "cardDes": '今天可能會面臨衝突或不和諧。保持冷靜，並且尋找解決爭端的方法。避免不必要的對抗。'},
    {"cardName": '寶劍五(The Five of Swords)逆位', "cardDes": '今天可能會感到爭執的緩解或結束。試著以和解的方式面對衝突，並且尋找共識。'},
    {"cardName": '寶劍六(The Six of Swords)正位', "cardDes": '今天是尋找平靜和過渡的好時機。離開困境，並且尋求新的機會和解決方案。'},
    {"cardName": '寶劍六(The Six of Swords)逆位', "cardDes": '今天可能會感到困難的過渡或掙扎。試著尋找支持，並且耐心面對挑戰。'},
    {"cardName": '寶劍七(The Seven of Swords)正位', "cardDes": '今天可能會面臨隱藏的問題或需要謹慎行事。保持警覺，並且尋找真相。'},
    {"cardName": '寶劍七(The Seven of Swords)逆位', "cardDes": '今天可能會感到誠實和透明的釋放。試著直面問題，並且尋找誠實的解決方案。'},
    {"cardName": '寶劍八(The Eight of Swords)正位', "cardDes": '今天可能會感到被束縛或困在限制中。試著重新評估你的選擇，並且尋找解放的方法。'},
    {"cardName": '寶劍八(The Eight of Swords)逆位', "cardDes": '今天可能會開始感覺到束縛的解除。尋找新的可能性，並且勇敢地面對挑戰。'},
    {"cardName": '寶劍九(The Nine of Swords)正位', "cardDes": '今天可能會感到焦慮或擔憂。試著找到放鬆的方法，並且避免過度擔憂。'},
    {"cardName": '寶劍九(The Nine of Swords)逆位', "cardDes": '今天可能會感到焦慮減輕或情緒得到舒緩。試著尋找正向的思考方式，並且關注自我照顧。'},
    {"cardName": '寶劍十(The Ten of Swords)正位', "cardDes": '今天可能會感到結束或失望。試著接受過去的經歷，並且尋找新的開始。'},
    {"cardName": '寶劍十(The Ten of Swords)逆位', "cardDes": '今天可能會開始從困難中恢復。尋找新的機會，並且感恩過去的經歷。'},
    {"cardName": '寶劍侍者(The Page of Swords)正位', "cardDes": '今天適合探索新的想法和學習。保持好奇心，並且尋找新的知識。'},
    {"cardName": '寶劍侍者(The Page of Swords)逆位', "cardDes": '今天可能會感到缺乏清晰或面臨誤解。試著重新思考你的觀點，並且尋求清晰的溝通。'},
    {"cardName": '寶劍騎士(The Knight of Swords)正位', "cardDes": '今天適合快速行動和追求目標。保持果斷，並且勇敢地面對挑戰。'},
    {"cardName": '寶劍騎士(The Knight of Swords)逆位', "cardDes": '今天可能會感到衝動或計劃不周的困難。試著保持冷靜，並且重新評估你的行動。'},
    {"cardName": '寶劍女王(The Queen of Swords)正位', "cardDes": '今天適合清晰地表達你的想法和觀點。保持理智，並且用智慧來解決問題。'},
    {"cardName": '寶劍女王(The Queen of Swords)逆位', "cardDes": '今天可能會感到情感上的冷漠或困惑。試著尋找情感上的平衡，並且避免過度分析。'},
    {"cardName": '寶劍國王(The King of Swords)正位', "cardDes": '今天適合展現你的智慧和領導力。用理智和策略來解決問題，並且保持公正。'},
    {"cardName": '寶劍國王(The King of Swords)逆位', "cardDes": '今天可能會面臨判斷上的困難或道德挑戰。試著保持正直，並且尋找公正的解決方案。'},
    {"cardName": '錢幣一(The Ace of Pentacles)正位', "cardDes": '今天是開始新的財務或實質項目的好時機。抓住機會，並且專注於你的目標。'},
    {"cardName": '錢幣一(The Ace of Pentacles)逆位', "cardDes": '今天可能會感到財務上的困難或機會的錯失。試著重新評估你的計劃，並且尋找解決方案。'},
    {"cardName": '錢幣二(The Two of Pentacles)正位', "cardDes": '今天適合平衡你的工作和生活。保持靈活，並且管理好你的資源。'},
    {"cardName": '錢幣二(The Two of Pentacles)逆位', "cardDes": '今天可能會感到平衡上的困難或忙碌。試著重新評估你的優先事項，並且尋找平衡的方法。'},
    {"cardName": '錢幣三(The Three of Pentacles)正位', "cardDes": '今天是合作和實現共同目標的好時機。尋找團隊合作的機會，並且發揮你的專業技能。'},
    {"cardName": '錢幣三(The Three of Pentacles)逆位', "cardDes": '今天可能會面臨合作上的挑戰或缺乏支持。試著尋找解決方案，並且建立良好的溝通。'},
    {"cardName": '錢幣四(The Four of Pentacles)正位', "cardDes": '今天適合管理你的財務和資源。保持穩定，並且避免過度保守。'},
    {"cardName": '錢幣四(The Four of Pentacles)逆位', "cardDes": '今天可能會感到財務上的不穩定或控制上的困難。試著尋找支持，並且重新評估你的財務狀況。'},
    {"cardName": '錢幣五(The Five of Pentacles)正位', "cardDes": '今天可能會感到經濟上的挑戰或困難。尋找支持，並且保持信心。'},
    {"cardName": '錢幣五(The Five of Pentacles)逆位', "cardDes": '今天可能會感到經濟困難的緩解。尋找積極的解決方案，並且感激你的資源。'},
    {"cardName": '錢幣六(The Six of Pentacles)正位', "cardDes": '今天適合慷慨和分享。尋找回報和支持，並且幫助他人。'},
    {"cardName": '錢幣六(The Six of Pentacles)逆位', "cardDes": '今天可能會感到不公平或經濟上的困難。試著尋找平衡，並且避免過度依賴他人。'},
    {"cardName": '錢幣七(The Seven of Pentacles)正位', "cardDes": '今天是檢視和評估你的進展的時刻。尋找長期的成果，並且保持耐心。'},
    {"cardName": '錢幣七(The Seven of Pentacles)逆位', "cardDes": '今天可能會感到進展緩慢或失望。試著重新評估你的策略，並且保持信心。'},
    {"cardName": '錢幣八(The Eight of Pentacles)正位', "cardDes": '今天適合專注於工作和技能的提升。投入努力，並且尋求專業上的進步。'},
    {"cardName": '錢幣八(The Eight of Pentacles)逆位', "cardDes": '今天可能會感到工作上的困難或缺乏動力。試著重新激勵自己，並且尋找改進的方式。'},
    {"cardName": '錢幣九(The Nine of Pentacles)正位', "cardDes": '今天是享受成果和財務穩定的時刻。感受你的成功，並且珍惜你所擁有的。'},
    {"cardName": '錢幣九(The Nine of Pentacles)逆位', "cardDes": '今天可能會感到財務上的挑戰或不滿。試著重新評估你的目標，並且尋找解決方案。'},
    {"cardName": '錢幣十(The Ten of Pentacles)正位', "cardDes": '今天適合建立長期的安全感和穩定。與家人和社群分享你的成功，並且感受成就。'},
    {"cardName": '錢幣十(The Ten of Pentacles)逆位', "cardDes": '今天可能會感到穩定性的挑戰或家庭上的困難。試著尋找解決方案，並且關注長期的目標。'},
    {"cardName": '錢幣侍者(The Page of Pentacles)正位', "cardDes": '今天適合學習和發展新的技能。保持好奇心，並且尋找增長的機會。'},
    {"cardName": '錢幣侍者(The Page of Pentacles)逆位', "cardDes": '今天可能會感到學習上的困難或缺乏動力。試著尋找支持，並且重新激勵自己。'},
    {"cardName": '錢幣騎士(The Knight of Pentacles)正位', "cardDes": '今天適合踏實地工作和追求目標。保持耐心，並且專注於長期的計劃。'},
    {"cardName": '錢幣騎士(The Knight of Pentacles)逆位', "cardDes": '今天可能會感到計劃上的困難或缺乏進展。試著重新評估你的策略，並且保持信心。'},
    {"cardName": '錢幣女王(The Queen of Pentacles)正位', "cardDes": '今天適合關注你的家庭和實際需求。保持關懷，並且尋求生活中的穩定。'},
    {"cardName": '錢幣女王(The Queen of Pentacles)逆位', "cardDes": '今天可能會感到實際上的困難或不穩定。試著尋找支持，並且重新評估你的需求。'},
    {"cardName": '錢幣國王(The King of Pentacles)正位', "cardDes": '今天適合展現你的財務智慧和穩定。管理好你的資源，並且發揮領導力。'},
    {"cardName": '錢幣國王(The King of Pentacles)逆位', "cardDes": '今天可能會感到財務上的挑戰或控制上的困難。試著尋找平衡，並且重新評估你的財務策略。'},
    {"cardName": '權杖一(The Ace of Wands)正位', "cardDes": '今天是開始新計劃和追求創意的好時機。保持熱情，並且勇敢地面對挑戰。'},
    {"cardName": '權杖一(The Ace of Wands)逆位', "cardDes": '今天可能會感到缺乏創意或阻礙。試著重新激勵自己，並且尋找新的靈感。'},
    {"cardName": '權杖二(The Two of Wands)正位', "cardDes": '今天適合制定長期計劃和展望未來。保持遠見，並且尋找機會來實現目標。'},
    {"cardName": '權杖二(The Two of Wands)逆位', "cardDes": '今天可能會感到計劃上的困難或不確定。試著尋找明確的方向，並且保持靈活。'},
    {"cardName": '權杖三(The Three of Wands)正位', "cardDes": '今天是等待成果和尋找新機會的時刻。保持耐心，並且準備迎接新的挑戰。'},
    {"cardName": '權杖三(The Three of Wands)逆位', "cardDes": '今天可能會感到進展緩慢或缺乏前進的方向。試著重新評估你的計劃，並且尋找新的機會。'},
    {"cardName": '權杖四(The Four of Wands)正位', "cardDes": '今天是慶祝成功和享受穩定的時刻。與他人分享你的成就，並且感受喜悅。'},
    {"cardName": '權杖四(The Four of Wands)逆位', "cardDes": '今天可能會感到穩定性上的挑戰或家庭上的問題。試著尋找解決方案，並且關注關係中的和諧。'},
    {"cardName": '權杖五(The Five of Wands)正位', "cardDes": '今天可能會面臨競爭或衝突。保持冷靜，並且尋找合作的方式來解決問題。'},
    {"cardName": '權杖五(The Five of Wands)逆位', "cardDes": '今天可能會感到衝突的緩解或解決。試著尋找和平的方式來處理爭端，並且促進合作。'},
    {"cardName": '權杖六(The Six of Wands)正位', "cardDes": '今天是慶祝勝利和成就的時刻。享受你的成功，並且感受到自信和驕傲。'},
    {"cardName": '權杖六(The Six of Wands)逆位', "cardDes": '今天可能會感到成功上的挑戰或缺乏認可。試著保持信心，並且尋找內在的驕傲。'},
    {"cardName": '權杖七(The Seven of Wands)正位', "cardDes": '今天適合捍衛你的立場和面對挑戰。保持堅定，並且勇敢地面對困難。'},
    {"cardName": '權杖七(The Seven of Wands)逆位', "cardDes": '今天可能會感到挑戰上的困難或過度防守。試著找到平衡，並且尋找支持。'},
    {"cardName": '權杖八(The Eight of Wands)正位', "cardDes": '今天是迅速行動和迎接變化的好時機。保持靈活，並且勇敢地追求你的目標。'},
    {"cardName": '權杖八(The Eight of Wands)逆位', "cardDes": '今天可能會感到行動上的困難或延遲。試著尋找解決方案，並且保持耐心。'},
    {"cardName": '權杖九(The Nine of Wands)正位', "cardDes": '今天是堅持和面對挑戰的時刻。保持耐心，並且勇敢地面對困難。'},
    {"cardName": '權杖九(The Nine of Wands)逆位', "cardDes": '今天可能會感到疲憊或難以繼續。試著尋找支持，並且關注自我照顧。'},
    {"cardName": '權杖十(The Ten of Wands)正位', "cardDes": '今天可能會感到責任上的重擔或壓力。試著分擔工作，並且尋找輕鬆的方法。'},
    {"cardName": '權杖十(The Ten of Wands)逆位', "cardDes": '今天可能會感到負擔減輕或壓力的緩解。尋找平衡，並且感激你的努力。'},
    {"cardName": '權杖侍者(The Page of Wands)正位', "cardDes": '今天適合追求新的創意和熱情。保持好奇心，並且勇敢地探索新的領域。'},
    {"cardName": '權杖侍者(The Page of Wands)逆位', "cardDes": '今天可能會感到創意上的阻礙或動力不足。試著重新激勵自己，並且尋找新的靈感。'},
    {"cardName": '權杖騎士(The Knight of Wands)正位', "cardDes": '今天適合快速行動和追求你的激情。保持決心，並且勇敢地迎接挑戰。'},
    {"cardName": '權杖騎士(The Knight of Wands)逆位', "cardDes": '今天可能會感到衝動或計劃上的困難。試著保持冷靜，並且重新評估你的目標。'},
    {"cardName": '權杖女王(The Queen of Wands)正位', "cardDes": '今天適合展現你的創意和魅力。保持自信，並且發揮你的領導力。'},
    {"cardName": '權杖女王(The Queen of Wands)逆位', "cardDes": '今天可能會感到自信不足或創意上的困難。試著尋找支持，並且重新激發你的熱情。'},
    {"cardName": '權杖國王(The King of Wands)正位', "cardDes": '今天適合展現你的領導力和創意。保持積極，並且勇敢地面對挑戰。'},
    {"cardName": '權杍國王(The King of Wands)逆位', "cardDes": '今天可能會感到領導力上的挑戰或過度的控制。試著尋找平衡，並且尋求支持。'}
]

care =[
    {"cardName":'愚者(The Fool)正位',"cardDes":'正位的愚者象徵著無限的潛力和新的開始。在心理照護中，它提醒人們接受新的機會，保持開放的心態，並相信自己的直覺。這張牌代表著勇氣與探索的精神。'},
    {"cardName":'愚者(The Fool)逆位',"cardDes":'逆位的愚者可能暗示著衝動、不負責任或對新事物的恐懼。在心理照護中，它建議人們在做決定時保持謹慎，避免魯莽行為。這張牌可能反映了不安感，需要自我反省來找到內心的平衡。'},

    {"cardName":'魔術師(The Magician)正位',"cardDes":'正位的魔術師代表著行動力、創造力和掌握資源的能力。在心理照護中，這張牌鼓勵人們相信自己的能力，利用所擁有的資源來實現目標。這是一張強調自我掌控和專注的牌。'},
    {"cardName":'魔術師(The Magician)逆位',"cardDes":'逆位的魔術師可能意味著欺騙、錯誤的判斷或缺乏信心。在心理照護中，它提醒人們警惕周圍的詐欺行為，或是對自己的能力有清醒的認識。這張牌可能暗示需要重新審視自己的目標和計劃。'},

    {"cardName":'女祭司(The High Priestess)正位',"cardDes":'正位的女祭司象徵著直覺、神秘和內在智慧。在心理照護中，這張牌鼓勵人們傾聽內心的聲音，信任自己的直覺。它是一張強調內在成長與精神探索的牌。'},
    {"cardName":'女祭司(The High Priestess)逆位',"cardDes":'逆位的女祭司可能代表隱藏的真相、不安或內心的困惑。在心理照護中，這張牌建議人們需要更多的自我反省和理解，避免過度依賴外部意見。它可能暗示需要深入探索自己的潛意識。'},

    {"cardName":'皇后(The Empress)正位',"cardDes":'正位的皇后代表著豐饒、愛與創造力。在心理照護中，這張牌強調自我照顧、培養和愛的力量。它鼓勵人們關注身心健康，並且與他人建立有愛的關係。'},
    {"cardName":'皇后(The Empress)逆位',"cardDes":'逆位的皇后可能暗示著創造力的受阻、情感的冷漠或過度的依賴。在心理照護中，這張牌提醒人們要重視自我價值，避免忽略自己的情感需求。它可能暗示需要恢復與內在自我的連結。'},
    
     {"cardName":'皇帝(The Emperor)正位',"cardDes":'正位的皇帝象徵著秩序、穩定和權威。在心理照護中，這張牌強調建立結構和界限的重要性。它鼓勵人們在生活中尋求穩定，並在需要時展現領導能力。'},
    {"cardName":'皇帝(The Emperor)逆位',"cardDes":'逆位的皇帝可能代表著過度控制、專制或缺乏紀律。在心理照護中，這張牌提醒人們放鬆過度的控制欲，學會信任他人，並避免過於固執。'},

    {"cardName":'教皇(The Hierophant)正位',"cardDes":'正位的教皇象徵著傳統、信仰和指導。在心理照護中，這張牌強調追求精神或道德的成長，並鼓勵人們從他人那裡尋求指導或教育。'},
    {"cardName":'教皇(The Hierophant)逆位',"cardDes":'逆位的教皇可能意味著質疑傳統、反叛或精神上的困惑。在心理照護中，這張牌提醒人們要找到自己的道路，並勇於質疑不再適用的信仰或習慣。'},

    {"cardName":'戀人(The Lovers)正位',"cardDes":'正位的戀人代表愛、和諧和選擇。在心理照護中，這張牌強調建立深厚關係的重要性，並鼓勵人們做出符合內心價值觀的選擇。'},
    {"cardName":'戀人(The Lovers)逆位',"cardDes":'逆位的戀人可能暗示著關係中的分歧、錯誤的選擇或內心的矛盾。在心理照護中，這張牌提醒人們要正視關係中的問題，並重新審視自己的決定。'},

    {"cardName":'戰車(The Chariot)正位',"cardDes":'正位的戰車象徵著意志力、勝利和決心。在心理照護中，這張牌鼓勵人們保持專注，並利用強大的意志力克服挑戰。它代表著在困難面前前進的能力。'},
    {"cardName":'戰車(The Chariot)逆位',"cardDes":'逆位的戰車可能意味著缺乏方向、失敗或內心的衝突。在心理照護中，這張牌提醒人們在追求目標時需要明確的計劃，並避免被內在或外在的衝突所困擾。'},

    {"cardName":'力量(Strength)正位',"cardDes":'正位的力量代表內心的勇氣、耐心和同情。在心理照護中，這張牌強調以平和的方式面對困難，並相信自己的內在力量。它鼓勵人們通過柔和和堅定來克服挑戰。'},
    {"cardName":'力量(Strength)逆位',"cardDes":'逆位的力量可能暗示著恐懼、自我懷疑或控制力的缺乏。在心理照護中，這張牌提醒人們要認識並接納自己的弱點，並且學會用愛和耐心來對待自己和他人。'},

    {"cardName":'隱士(The Hermit)正位',"cardDes":'正位的隱士象徵著內省、智慧和獨立。在心理照護中，這張牌強調自我反省的重要性，並鼓勵人們尋找內心的真理。它是一張代表靜心與個人成長的牌。'},
    {"cardName":'隱士(The Hermit)逆位',"cardDes":'逆位的隱士可能意味著孤立、自我封閉或對內在問題的逃避。在心理照護中，這張牌提醒人們要保持與外界的聯繫，並避免陷入孤立或過度自省。'},

    {"cardName":'命運之輪(The Wheel of Fortune)正位',"cardDes":'正位的命運之輪象徵著變化、機會和循環。在心理照護中，這張牌強調接受生命中的起伏，並相信變化帶來的機會。它是一張鼓勵人們隨遇而安的牌。'},
    {"cardName":'命運之輪(The Wheel of Fortune)逆位',"cardDes":'逆位的命運之輪可能暗示著逆境、不順或失去控制感。在心理照護中，這張牌提醒人們在困難時期保持冷靜，並尋求新的機會來重新掌控局勢。'},
    
    
    
    
    
     {"cardName":'正義(Justice)正位',"cardDes":'正位的正義象徵公平、真理和因果報應。在心理照護中，這張牌強調做出符合道德和倫理的選擇，並且承擔自己的行為後果。它鼓勵人們追求真理，並在生活中保持公正。'},
    {"cardName":'正義(Justice)逆位',"cardDes":'逆位的正義可能暗示著不公平、偏見或拒絕承擔責任。在心理照護中，這張牌提醒人們正視自己行為的後果，並且尋求修正不公平的情況。'},

    {"cardName":'吊人(The Hanged Man)正位',"cardDes":'正位的吊人象徵著犧牲、靜止和新的觀點。在心理照護中，這張牌強調接受暫時的停滯，並利用這段時間來重新審視生命中的各種觀點。它是一張鼓勵人們放下控制，接受現實的牌。'},
    {"cardName":'吊人(The Hanged Man)逆位',"cardDes":'逆位的吊人可能意味著拒絕變化、僵化或被困在不利的情境中。在心理照護中，這張牌提醒人們要避免過度固執，並尋求新的方式來突破困境。'},

    {"cardName":'死神(Death)正位',"cardDes":'正位的死神象徵著結束、轉變和新生。在心理照護中，這張牌強調接受生命中的自然變化，並從過去的經歷中成長。它是一張鼓勵人們釋放舊有的包袱，迎接新的開始的牌。'},
    {"cardName":'死神(Death)逆位',"cardDes":'逆位的死神可能暗示著恐懼變化、抗拒結束或困在過去。在心理照護中，這張牌提醒人們需要接受變化，並且勇敢地面對結束帶來的挑戰。'},

    {"cardName":'節制(Temperance)正位',"cardDes":'正位的節制象徵著平衡、和諧和節制。在心理照護中，這張牌強調生活中的平衡與協調，並且鼓勵人們在情緒、行為和思維上保持中庸之道。它是一張強調和諧共處與自我調整的牌。'},
    {"cardName":'節制(Temperance)逆位',"cardDes":'逆位的節制可能意味著失衡、極端或不安定。在心理照護中，這張牌提醒人們要注意生活中的過度行為，並且努力恢復內心和外界的平衡。'},

    {"cardName":'魔鬼(The Devil)正位',"cardDes":'正位的魔鬼象徵著誘惑、束縛和物質的執著。在心理照護中，這張牌提醒人們要警惕過度依賴或沉迷於物質和快樂中。它是一張鼓勵人們打破限制，尋找自由的牌。'},
    {"cardName":'魔鬼(The Devil)逆位',"cardDes":'逆位的魔鬼可能暗示著擺脫束縛、克服誘惑或內在的解放。在心理照護中，這張牌強調釋放內在的恐懼與限制，並且勇敢地面對自己的陰暗面。'},

    {"cardName":'塔(The Tower)正位',"cardDes":'正位的塔象徵著突然的變革、破壞和清洗。在心理照護中，這張牌強調接受生活中的劇變，並從中尋找成長的機會。它是一張提醒人們在逆境中找到新方向的牌。'},
    {"cardName":'塔(The Tower)逆位',"cardDes":'逆位的塔可能意味著避免災難、抵抗變革或恐懼。在心理照護中，這張牌提醒人們不要害怕改變，並且勇於迎接必要的重建。'},

    {"cardName":'星星(The Star)正位',"cardDes":'正位的星星象徵著希望、靈感和精神的指引。在心理照護中，這張牌鼓勵人們保持樂觀，並相信未來會有更好的發展。它是一張代表療癒與重生的牌。'},
    {"cardName":'星星(The Star)逆位',"cardDes":'逆位的星星可能暗示著失望、絕望或靈感的缺乏。在心理照護中，這張牌提醒人們即使在困難時期也要保持希望，並尋求內在的指引。'},

    {"cardName":'月亮(The Moon)正位',"cardDes":'正位的月亮象徵著潛意識、幻象和內在的恐懼。在心理照護中，這張牌強調探索內在世界的重要性，並提醒人們要面對和理解自己的恐懼和疑慮。'},
    {"cardName":'月亮(The Moon)逆位',"cardDes":'逆位的月亮可能意味著困惑、欺騙或情緒的不穩定。在心理照護中，這張牌提醒人們要警惕周圍的虛假信息，並努力保持情緒上的穩定。'},

    {"cardName":'太陽(The Sun)正位',"cardDes":'正位的太陽象徵著快樂、成功和生命力。在心理照護中，這張牌鼓勵人們積極面對生活，並享受每一刻的幸福。它是一張代表快樂和成就的牌。'},
    {"cardName":'太陽(The Sun)逆位',"cardDes":'逆位的太陽可能暗示著自滿、過度樂觀或對現實的忽視。在心理照護中，這張牌提醒人們不要忽略潛在的問題，並且保持對現實的清醒認識。'},

    {"cardName":'審判(Judgement)正位',"cardDes":'正位的審判象徵著覺醒、復活和內在的呼喚。在心理照護中，這張牌強調自我評估和精神的提升，並鼓勵人們聆聽內心的召喚，追求更高的目標。'},
    {"cardName":'審判(Judgement)逆位',"cardDes":'逆位的審判可能意味著自我懷疑、逃避責任或過去的困擾。在心理照護中，這張牌提醒人們正視自己的錯誤，並且勇於面對過去以尋求救贖。'},

    {"cardName":'世界(The World)正位',"cardDes":'正位的世界象徵著完成、成就和圓滿。在心理照護中，這張牌鼓勵人們慶祝自己的成功，並且接受生命中的新階段。它是一張代表圓滿與達成目標的牌。'},
    {"cardName":'世界(The World)逆位',"cardDes":'逆位的世界可能暗示著未完成、停滯或缺乏成就感。在心理照護中，這張牌提醒人們需要完成未竟之事，並且努力打破阻礙前進的障礙。'},
    
    {"cardName":'權杖一(Ace of Wands)正位',"cardDes":'正位的權杖一象徵著新開始、創意和活力。在心理照護中，這張牌鼓勵人們追求新的目標或項目，並且相信自己的創造力和活力能夠帶來成功。'},
    {"cardName":'權杖一(Ace of Wands)逆位',"cardDes":'逆位的權杖一可能意味著創意阻塞、動力不足或猶豫不決。在心理照護中，這張牌提醒人們找到重新點燃激情的方法，並克服內心的障礙。'},

    {"cardName":'權杖二(Two of Wands)正位',"cardDes":'正位的權杖二象徵著計劃、展望和決策。在心理照護中，這張牌強調制定長期計劃的重要性，並鼓勵人們勇於冒險並探索新的機會。'},
    {"cardName":'權杖二(Two of Wands)逆位',"cardDes":'逆位的權杖二可能暗示著優柔寡斷、害怕改變或計劃不周。在心理照護中，這張牌提醒人們要自信地做出決策，並避免因猶豫而錯失良機。'},

    {"cardName":'權杖三(Three of Wands)正位',"cardDes":'正位的權杖三象徵著擴展、冒險和遠見。在心理照護中，這張牌鼓勵人們展望未來，並相信自己的努力會帶來豐收。它是一張提醒人們擴展視野的牌。'},
    {"cardName":'權杖三(Three of Wands)逆位',"cardDes":'逆位的權杖三可能意味著延誤、挫折或缺乏計劃。在心理照護中，這張牌提醒人們要檢查自己的計劃，並準備好應對可能的挑戰。'},

    {"cardName":'權杖四(Four of Wands)正位',"cardDes":'正位的權杖四象徵著慶祝、穩定和家庭幸福。在心理照護中，這張牌強調家庭和社交關係的重要性，並鼓勵人們享受生活中的歡樂時光。'},
    {"cardName":'權杖四(Four of Wands)逆位',"cardDes":'逆位的權杖四可能暗示著家庭或社交關係中的不和諧、不安或爭吵。在心理照護中，這張牌提醒人們需要解決家庭或社交圈中的問題，並努力恢復和諧。'},

    {"cardName":'權杖五(Five of Wands)正位',"cardDes":'正位的權杖五象徵著競爭、衝突和挑戰。在心理照護中，這張牌強調健康競爭的價值，並鼓勵人們通過挑戰來提升自己。'},
    {"cardName":'權杖五(Five of Wands)逆位',"cardDes":'逆位的權杖五可能意味著逃避衝突、壓抑或內心的緊張。在心理照護中，這張牌提醒人們正視問題，並尋找解決衝突的建設性方法。'},

    {"cardName":'權杖六(Six of Wands)正位',"cardDes":'正位的權杖六象徵著勝利、認可和自信。在心理照護中，這張牌鼓勵人們慶祝自己的成功，並相信自己的能力。它是一張鼓勵自信與成就的牌。'},
    {"cardName":'權杖六(Six of Wands)逆位',"cardDes":'逆位的權杖六可能暗示著自我懷疑、失敗或缺乏認可。在心理照護中，這張牌提醒人們不要因短暫的挫折而失去信心，並持續努力達成目標。'},

    {"cardName":'權杖七(Seven of Wands)正位',"cardDes":'正位的權杖七象徵著防禦、挑戰和堅持。在心理照護中，這張牌鼓勵人們在面對困難時保持堅定，並捍衛自己的立場。'},
    {"cardName":'權杖七(Seven of Wands)逆位',"cardDes":'逆位的權杖七可能意味著缺乏防備、退縮或壓力。在心理照護中，這張牌提醒人們要保持警惕，並避免因壓力過大而退縮。'},

    {"cardName":'權杖八(Eight of Wands)正位',"cardDes":'正位的權杖八象徵著速度、進展和溝通。在心理照護中，這張牌強調迅速行動的重要性，並鼓勵人們抓住機會，快速達成目標。'},
    {"cardName":'權杖八(Eight of Wands)逆位',"cardDes":'逆位的權杖八可能暗示著延誤、混亂或溝通不暢。在心理照護中，這張牌提醒人們要耐心應對障礙，並努力改善溝通。'},

    {"cardName":'權杖九(Nine of Wands)正位',"cardDes":'正位的權杖九象徵著堅韌、準備和防禦。在心理照護中，這張牌強調在面對困難時保持堅韌，並為未來的挑戰做好準備。'},
    {"cardName":'權杖九(Nine of Wands)逆位',"cardDes":'逆位的權杖九可能意味著疲憊、放棄或過度防禦。在心理照護中，這張牌提醒人們要注意自己的心理和身體狀況，避免過度勞累。'},

    {"cardName":'權杖十(Ten of Wands)正位',"cardDes":'正位的權杖十象徵著責任、負擔和努力。在心理照護中，這張牌提醒人們要學會管理壓力，並在必要時尋求幫助。它強調在困難中保持堅持的重要性。'},
    {"cardName":'權杖十(Ten of Wands)逆位',"cardDes":'逆位的權杖十可能暗示著過度壓力、無法承受的負擔或被責任壓垮。在心理照護中，這張牌提醒人們需要釋放壓力，並適時減少過重的負擔。'},

    {"cardName":'權杖侍者(Page of Wands)正位',"cardDes":'正位的權杖侍者象徵著好奇心、冒險精神和新機會。在心理照護中，這張牌鼓勵人們探索新的事物，並相信自己的潛力。'},
    {"cardName":'權杖侍者(Page of Wands)逆位',"cardDes":'逆位的權杖侍者可能意味著不確定、遲疑或缺乏方向。在心理照護中，這張牌提醒人們需要找到內在的動力，並避免因恐懼而停滯不前。'},

    {"cardName":'權杖騎士(Knight of Wands)正位',"cardDes":'正位的權杖騎士象徵著行動力、熱情和冒險。在心理照護中，這張牌鼓勵人們勇敢追求自己的夢想，並保持積極的心態。'},
    {"cardName":'權杖騎士(Knight of Wands)逆位',"cardDes":'逆位的權杖騎士可能暗示著衝動、莽撞或缺乏計劃。在心理照護中，這張牌提醒人們要避免過於衝動，並在行動前仔細計劃。'},

    {"cardName":'權杖皇后(Queen of Wands)正位',"cardDes":'正位的權杖皇后象徵著自信、活力和領導力。在心理照護中，這張牌鼓勵人們發揮自己的領導能力，並以積極的態度面對挑戰。'},
    {"cardName":'權杖皇后(Queen of Wands)逆位',"cardDes":'逆位的權杖皇后可能意味著不安全感、懷疑或自我懷疑。在心理照護中，這張牌提醒人們要增強自信，並相信自己的能力。'},

    {"cardName":'權杖國王(King of Wands)正位',"cardDes":'正位的權杖國王象徵著領導力、智慧和成功。在心理照護中，這張牌鼓勵人們發揮自己的領導才能，並以智慧引導他人。'},
    {"cardName":'權杖國王(King of Wands)逆位',"cardDes":'逆位的權杖國王可能暗示著獨裁、傲慢或濫用權力。在心理照護中，這張牌提醒人們要謹慎使用自己的影響力，並避免過度控制他人。'},
    
    
    
    {"cardName":'聖杯一(Ace of Cups)正位',"cardDes":'正位的聖杯一象徵著愛、情感和新的人際關係。在心理照護中，這張牌鼓勵人們打開心扉，接受愛與情感的流動，並培養深厚的情感聯繫。'},
    {"cardName":'聖杯一(Ace of Cups)逆位',"cardDes":'逆位的聖杯一可能意味著情感阻塞、愛的缺失或關係中的困難。在心理照護中，這張牌提醒人們要處理未解決的情感問題，並學會愛自己。'},

    {"cardName":'聖杯二(Two of Cups)正位',"cardDes":'正位的聖杯二象徵著愛情、合作與和諧。在心理照護中，這張牌鼓勵人們建立和諧的人際關係，並重視人際間的互相支持與合作。'},
    {"cardName":'聖杯二(Two of Cups)逆位',"cardDes":'逆位的聖杯二可能暗示著人際關係中的不和、誤解或分離。在心理照護中，這張牌提醒人們要處理衝突，並努力恢復關係中的平衡。'},

    {"cardName":'聖杯三(Three of Cups)正位',"cardDes":'正位的聖杯三象徵著慶祝、友誼和社交活動。在心理照護中，這張牌強調社交圈的重要性，並鼓勵人們與朋友和家人共同慶祝生活中的美好時刻。'},
    {"cardName":'聖杯三(Three of Cups)逆位',"cardDes":'逆位的聖杯三可能意味著孤立、友誼的失落或社交活動中的困難。在心理照護中，這張牌提醒人們要重新審視自己的人際關係，並尋找新的社交支持系統。'},

    {"cardName":'聖杯四(Four of Cups)正位',"cardDes":'正位的聖杯四象徵著沉思、內省和情感上的不滿。在心理照護中，這張牌提醒人們要花時間了解自己的情感需求，並避免陷入無法滿足的情感狀態中。'},
    {"cardName":'聖杯四(Four of Cups)逆位',"cardDes":'逆位的聖杯四可能暗示著情感上的困惑、錯過機會或過於執著過去。在心理照護中，這張牌鼓勵人們放下過去的執念，並尋找新的情感機會。'},

    {"cardName":'聖杯五(Five of Cups)正位',"cardDes":'正位的聖杯五象徵著失落、悲傷和後悔。在心理照護中，這張牌提醒人們要接受和處理失去的感覺，並學會從悲傷中學習和成長。'},
    {"cardName":'聖杯五(Five of Cups)逆位',"cardDes":'逆位的聖杯五可能意味著康復、情感的釋放或對過去的放手。在心理照護中，這張牌鼓勵人們放下過去，並展望未來的希望。'},

    {"cardName":'聖杯六(Six of Cups)正位',"cardDes":'正位的聖杯六象徵著懷舊、童年回憶和純真。在心理照護中，這張牌鼓勵人們回憶美好的過去，並從中尋找溫暖和安慰。'},
    {"cardName":'聖杯六(Six of Cups)逆位',"cardDes":'逆位的聖杯六可能暗示著過度沉溺於過去、難以向前或對現實的不滿。在心理照護中，這張牌提醒人們要學會放下過去，並在當下找到快樂。'},

    {"cardName":'聖杯七(Seven of Cups)正位',"cardDes":'正位的聖杯七象徵著幻想、選擇和困惑。在心理照護中，這張牌提醒人們在做出決定時要保持現實，避免被過多的選擇或幻想所迷惑。'},
    {"cardName":'聖杯七(Seven of Cups)逆位',"cardDes":'逆位的聖杯七可能意味著選擇困難、決策不當或現實與幻想的脫節。在心理照護中，這張牌鼓勵人們專注於具體的目標，並避免過於理想化。'},

    {"cardName":'聖杯八(Eight of Cups)正位',"cardDes":'正位的聖杯八象徵著放棄、尋找更深層次的滿足感或轉變。在心理照護中，這張牌提醒人們勇敢面對現實，並在必要時離開不再適合自己的情況。'},
    {"cardName":'聖杯八(Eight of Cups)逆位',"cardDes":'逆位的聖杯八可能暗示著對改變的抗拒、恐懼或放棄的猶豫。在心理照護中，這張牌提醒人們要面對現實，不要因為恐懼而停滯不前。'},

    {"cardName":'聖杯九(Nine of Cups)正位',"cardDes":'正位的聖杯九象徵著願望的實現、滿足和幸福。在心理照護中，這張牌鼓勵人們感恩並享受生活中的成就，並相信自己值得擁有幸福。'},
    {"cardName":'聖杯九(Nine of Cups)逆位',"cardDes":'逆位的聖杯九可能意味著過度的自滿、物質主義或內在的空虛。在心理照護中，這張牌提醒人們要重新審視自己的幸福來源，並避免過度追求外在的滿足。'},

    {"cardName":'聖杯十(Ten of Cups)正位',"cardDes":'正位的聖杯十象徵著家庭幸福、和諧和情感上的滿足。在心理照護中，這張牌強調家庭和親密關係的重要性，並鼓勵人們珍惜與家人共度的時光。'},
    {"cardName":'聖杯十(Ten of Cups)逆位',"cardDes":'逆位的聖杯十可能暗示著家庭不和、情感疏離或對理想家庭的失望。在心理照護中，這張牌提醒人們要解決家庭中的矛盾，並努力重建和諧的關係。'},

    {"cardName":'聖杯侍者(Page of Cups)正位',"cardDes":'正位的聖杯侍者象徵著純真、情感的開放和創意。在心理照護中，這張牌鼓勵人們打開心靈，並以充滿創意和同理心的方式表達自己的情感。'},
    {"cardName":'聖杯侍者(Page of Cups)逆位',"cardDes":'逆位的聖杯侍者可能意味著情感上的不成熟、混亂或過度的幻想。在心理照護中，這張牌提醒人們要更加現實地面對自己的情感需求，並學會情感的成熟表達。'},

    {"cardName":'聖杯騎士(Knight of Cups)正位',"cardDes":'正位的聖杯騎士象徵著浪漫、追求理想和真誠的感情。在心理照護中，這張牌鼓勵人們追求自己的情感目標，並以真誠的態度對待他人。'},
    {"cardName":'聖杯騎士(Knight of Cups)逆位',"cardDes":'逆位的聖杯騎士可能暗示著情感上的不穩定、猶豫或不切實際的期待。在心理照護中，這張牌提醒人們要保持情感上的穩定，並避免過度理想化他人或關係。'},

    {"cardName":'聖杯皇后(Queen of Cups)正位',"cardDes":'正位的聖杯皇后象徵著同理心、情感智慧和療癒。在心理照護中，這張牌強調自我關愛的重要性，並鼓勵人們關心自己的情感健康。'},
    {"cardName":'聖杯皇后(Queen of Cups)逆位',"cardDes":'逆位的聖杯皇后可能意味著情感上的混亂、依賴或情感過度。在心理照護中，這張牌提醒人們要學會平衡自己的情感需求，並避免過度依賴他人。'},

    {"cardName":'聖杯國王(King of Cups)正位',"cardDes":'正位的聖杯國王象徵著情感的平衡、智慧和慈悲。在心理照護中，這張牌強調情感控制和同理心的重要性，並鼓勵人們成為他人的情感支柱。'},
    {"cardName":'聖杯國王(King of Cups)逆位',"cardDes":'逆位的聖杯國王可能暗示著情感壓抑、冷漠或情感上的不平衡。在心理照護中，這張牌提醒人們要處理內在的情感問題，並學會健康地表達情感。'},
    
     {"cardName":'寶劍一(Ace of Swords)正位',"cardDes":'正位的寶劍一象徵著清晰的思維、真相和新觀點。在心理照護中，這張牌鼓勵人們追求真理，並保持頭腦清晰，做出明智的決策。'},
    {"cardName":'寶劍一(Ace of Swords)逆位',"cardDes":'逆位的寶劍一可能意味著混亂、誤解或缺乏方向。在心理照護中，這張牌提醒人們要解決內心的混亂，並重新找到思維的平衡。'},

    {"cardName":'寶劍二(Two of Swords)正位',"cardDes":'正位的寶劍二象徵著困境、選擇和內心的平衡。在心理照護中，這張牌鼓勵人們面對困難的選擇，並保持內心的和諧。'},
    {"cardName":'寶劍二(Two of Swords)逆位',"cardDes":'逆位的寶劍二可能暗示著逃避、壓抑或難以做出決定。在心理照護中，這張牌提醒人們要直面問題，並勇敢做出決定。'},

    {"cardName":'寶劍三(Three of Swords)正位',"cardDes":'正位的寶劍三象徵著心碎、失望和悲痛。在心理照護中，這張牌提醒人們要接受並處理痛苦的情感，並從中學會成長。'},
    {"cardName":'寶劍三(Three of Swords)逆位',"cardDes":'逆位的寶劍三可能意味著療癒、釋放痛苦或情感上的康復。在心理照護中，這張牌鼓勵人們放下過去的傷痛，並繼續前行。'},

    {"cardName":'寶劍四(Four of Swords)正位',"cardDes":'正位的寶劍四象徵著休息、恢復和內省。在心理照護中，這張牌強調休息的重要性，並鼓勵人們在壓力中尋找內心的平靜。'},
    {"cardName":'寶劍四(Four of Swords)逆位',"cardDes":'逆位的寶劍四可能暗示著不安、焦慮或無法放鬆。在心理照護中，這張牌提醒人們要重視心理健康，並給自己足夠的時間休息。'},

    {"cardName":'寶劍五(Five of Swords)正位',"cardDes":'正位的寶劍五象徵著衝突、敗北和失敗的教訓。在心理照護中，這張牌提醒人們要從衝突中學習，並避免無謂的爭鬥。'},
    {"cardName":'寶劍五(Five of Swords)逆位',"cardDes":'逆位的寶劍五可能意味著和解、放下衝突或避免爭端。在心理照護中，這張牌鼓勵人們尋求和平解決衝突，並放下過去的怨恨。'},

    {"cardName":'寶劍六(Six of Swords)正位',"cardDes":'正位的寶劍六象徵著過渡、改變和解脫。在心理照護中，這張牌強調從困境中移動的必要性，並鼓勵人們向前看，擁抱新的開始。'},
    {"cardName":'寶劍六(Six of Swords)逆位',"cardDes":'逆位的寶劍六可能暗示著抗拒改變、遲遲無法前行或陷入困境。在心理照護中，這張牌提醒人們要勇敢面對變化，並尋找出路。'},

    {"cardName":'寶劍七(Seven of Swords)正位',"cardDes":'正位的寶劍七象徵著策略、機智和獨立行動。在心理照護中，這張牌提醒人們要運用智慧來解決問題，並在必要時採取獨立的行動。'},
    {"cardName":'寶劍七(Seven of Swords)逆位',"cardDes":'逆位的寶劍七可能意味著揭露秘密、誠實或需要放棄某些不道德的行為。在心理照護中，這張牌鼓勵人們坦誠面對自己和他人，並放棄任何不誠實的行為。'},

    {"cardName":'寶劍八(Eight of Swords)正位',"cardDes":'正位的寶劍八象徵著束縛、困境和感覺無力。在心理照護中，這張牌提醒人們要意識到自我設限，並尋找方法擺脫困境。'},
    {"cardName":'寶劍八(Eight of Swords)逆位',"cardDes":'逆位的寶劍八可能暗示著解脫、擺脫束縛或重獲自由。在心理照護中，這張牌鼓勵人們打破內心的枷鎖，並尋求自我解放。'},

    {"cardName":'寶劍九(Nine of Swords)正位',"cardDes":'正位的寶劍九象徵著焦慮、恐懼和失眠。在心理照護中，這張牌提醒人們要面對自己的恐懼，並尋找健康的方式來處理焦慮。'},
    {"cardName":'寶劍九(Nine of Swords)逆位',"cardDes":'逆位的寶劍九可能意味著釋放恐懼、走出陰影或戰勝焦慮。在心理照護中，這張牌鼓勵人們克服內心的恐懼，並重獲平靜。'},

    {"cardName":'寶劍十(Ten of Swords)正位',"cardDes":'正位的寶劍十象徵著結束、背叛和徹底的改變。在心理照護中，這張牌提醒人們要接受生命中的結束，並準備迎接新的開始。'},
    {"cardName":'寶劍十(Ten of Swords)逆位',"cardDes":'逆位的寶劍十可能暗示著重新開始、康復或從困境中復原。在心理照護中，這張牌鼓勵人們放下過去的痛苦，並重新建立自己的生活。'},

    {"cardName":'寶劍侍者(Page of Swords)正位',"cardDes":'正位的寶劍侍者象徵著求知欲、警惕和靈敏。在心理照護中，這張牌強調學習和獲取知識的重要性，並鼓勵人們保持好奇心。'},
    {"cardName":'寶劍侍者(Page of Swords)逆位',"cardDes":'逆位的寶劍侍者可能意味著不穩定、過度批判或溝通問題。在心理照護中，這張牌提醒人們要保持溝通的清晰，並避免過度批評自己或他人。'},

    {"cardName":'寶劍騎士(Knight of Swords)正位',"cardDes":'正位的寶劍騎士象徵著行動、決斷力和追求真理。在心理照護中，這張牌鼓勵人們勇敢追求自己的理想，並迅速應對生活中的挑戰。'},
    {"cardName":'寶劍騎士(Knight of Swords)逆位',"cardDes":'逆位的寶劍騎士可能暗示著衝動、粗暴或缺乏計劃。在心理照護中，這張牌提醒人們要三思而後行，並避免衝動行事。'},

    {"cardName":'寶劍皇后(Queen of Swords)正位',"cardDes":'正位的寶劍皇后象徵著理智、獨立和清晰的判斷力。在心理照護中，這張牌強調理性思考的重要性，並鼓勵人們獨立處理問題。'},
    {"cardName":'寶劍皇后(Queen of Swords)逆位',"cardDes":'逆位的寶劍皇后可能意味著情感冷漠、過度批判或孤立。在心理照護中，這張牌提醒人們要平衡理性和情感，並避免過度孤立自己。'},

    {"cardName":'寶劍國王(King of Swords)正位',"cardDes":'正位的寶劍國王象徵著權威、智慧和公正。在心理照護中，這張牌強調公平和理智的重要性，並鼓勵人們堅持自己的信念。'},
    {"cardName":'寶劍國王(King of Swords)逆位',"cardDes":'逆位的寶劍國王可能暗示著獨裁、冷酷或不公平。在心理照護中，這張牌提醒人們要避免過度控制，並保持公正和理性。'},
    
    
    {"cardName":'權杖一(Ace of Wands)正位',"cardDes":'正位的權杖一象徵著創意、啟動和新機會。在心理照護中，這張牌鼓勵人們追求新的計劃和夢想，並用熱情和創造力啟動新的開始。'},
    {"cardName":'權杖一(Ace of Wands)逆位',"cardDes":'逆位的權杖一可能意味著創意的阻塞、計劃的延遲或動力不足。在心理照護中，這張牌提醒人們重新尋找自己的熱情，並解決阻礙進展的問題。'},

    {"cardName":'權杖二(Two of Wands)正位',"cardDes":'正位的權杖二象徵著未來的計劃、決策和擴展。在心理照護中，這張牌鼓勵人們展望未來，制定計劃，並勇敢地面對即將到來的挑戰。'},
    {"cardName":'權杖二(Two of Wands)逆位',"cardDes":'逆位的權杖二可能暗示著計劃的不確定、猶豫不決或進展緩慢。在心理照護中，這張牌提醒人們要克服不安，並明確自己的方向和目標。'},

    {"cardName":'權杖三(Three of Wands)正位',"cardDes":'正位的權杖三象徵著遠見、成功和等待成果。在心理照護中，這張牌提醒人們耐心等待，並相信自己所付出的努力將會得到回報。'},
    {"cardName":'權杖三(Three of Wands)逆位',"cardDes":'逆位的權杖三可能意味著延遲、錯過機會或計劃未能實現。在心理照護中，這張牌鼓勵人們檢討自己的計劃，並尋找解決方案。'},

    {"cardName":'權杖四(Four of Wands)正位',"cardDes":'正位的權杖四象徵著慶祝、和諧和完成。在心理照護中，這張牌鼓勵人們慶祝自己的成就，並享受生活中的和諧與安定。'},
    {"cardName":'權杖四(Four of Wands)逆位',"cardDes":'逆位的權杖四可能暗示著不安定、家庭不和或慶祝的失敗。在心理照護中，這張牌提醒人們重建和諧，並處理任何潛在的家庭或社交問題。'},

    {"cardName":'權杖五(Five of Wands)正位',"cardDes":'正位的權杖五象徵著競爭、挑戰和衝突。在心理照護中，這張牌提醒人們面對挑戰時要保持積極，並學會在競爭中尋找合作的機會。'},
    {"cardName":'權杖五(Five of Wands)逆位',"cardDes":'逆位的權杖五可能意味著衝突的化解、競爭的減少或不必要的爭執。在心理照護中，這張牌鼓勵人們尋求和平，並解決任何持續的衝突。'},

    {"cardName":'權杖六(Six of Wands)正位',"cardDes":'正位的權杖六象徵著勝利、成功和認可。在心理照護中，這張牌鼓勵人們自信地慶祝自己的成就，並接受來自他人的讚賞和認可。'},
    {"cardName":'權杖六(Six of Wands)逆位',"cardDes":'逆位的權杖六可能暗示著失敗、未能得到認可或自信的缺失。在心理照護中，這張牌提醒人們重建自信，並重新評估自己的成就。'},

    {"cardName":'權杖七(Seven of Wands)正位',"cardDes":'正位的權杖七象徵著堅持、挑戰和勇敢。在心理照護中，這張牌鼓勵人們在面對挑戰時要保持堅定，並勇敢捍衛自己的立場。'},
    {"cardName":'權杖七(Seven of Wands)逆位',"cardDes":'逆位的權杖七可能意味著退縮、放棄或面對挑戰的困難。在心理照護中，這張牌提醒人們要面對自己的恐懼，並找到勇氣迎接挑戰。'},

    {"cardName":'權杖八(Eight of Wands)正位',"cardDes":'正位的權杖八象徵著迅速的進展、變化和活動。在心理照護中，這張牌鼓勵人們保持積極，並迅速適應生活中的變化和挑戰。'},
    {"cardName":'權杖八(Eight of Wands)逆位',"cardDes":'逆位的權杖八可能暗示著延遲、停滯或計劃的變更。在心理照護中，這張牌提醒人們要接受生活中的變化，並找到前進的方式。'},

    {"cardName":'權杖九(Nine of Wands)正位',"cardDes":'正位的權杖九象徵著堅韌、耐心和防禦。在心理照護中，這張牌提醒人們要保持堅韌，並準備好應對即將到來的挑戰。'},
    {"cardName":'權杖九(Nine of Wands)逆位',"cardDes":'逆位的權杖九可能意味著疲憊、焦慮或對持續挑戰的困惑。在心理照護中，這張牌鼓勵人們放鬆自己，並尋求適當的休息和恢復。'},

    {"cardName":'權杖十(Ten of Wands)正位',"cardDes":'正位的權杖十象徵著負擔、責任和過度的壓力。在心理照護中，這張牌提醒人們要檢視自己的負擔，並學會分擔責任，避免過度壓力。'},
    {"cardName":'權杖十(Ten of Wands)逆位',"cardDes":'逆位的權杖十可能暗示著放下負擔、釋放壓力或重新安排生活。在心理照護中，這張牌鼓勵人們減少不必要的負擔，並尋找有效的壓力管理方式。'},

    {"cardName":'權杖侍者(Page of Wands)正位',"cardDes":'正位的權杖侍者象徵著探索、冒險和創新。在心理照護中，這張牌鼓勵人們勇敢探索新領域，並追求自己的熱情。'},
    {"cardName":'權杖侍者(Page of Wands)逆位',"cardDes":'逆位的權杖侍者可能意味著缺乏動力、方向不明或過於冒險。在心理照護中，這張牌提醒人們要清晰自己的目標，並避免無謂的冒險。'},

    {"cardName":'權杖騎士(Knight of Wands)正位',"cardDes":'正位的權杖騎士象徵著動力、熱情和冒險。在心理照護中，這張牌鼓勵人們以積極的態度追求自己的目標，並勇敢迎接挑戰。'},
    {"cardName":'權杖騎士(Knight of Wands)逆位',"cardDes":'逆位的權杖騎士可能暗示著衝動、過度冒險或缺乏方向。在心理照護中，這張牌提醒人們要控制衝動，並尋找穩定的方向。'},

    {"cardName":'權杖皇后(Queen of Wands)正位',"cardDes":'正位的權杖皇后象徵著自信、魅力和創造力。在心理照護中，這張牌鼓勵人們展現自信，並運用自己的創造力和魅力來實現目標。'},
    {"cardName":'權杖皇后(Queen of Wands)逆位',"cardDes":'逆位的權杖皇后可能意味著自我懷疑、過度主導或情感上的波動。在心理照護中，這張牌提醒人們要平衡自信和謙遜，並處理情感上的不穩定。'},

    {"cardName":'權杖國王(King of Wands)正位',"cardDes":'正位的權杖國王象徵著領導力、遠見和魅力。在心理照護中，這張牌強調領導力和遠見的重要性，並鼓勵人們以積極的方式影響他人。'},
    {"cardName":'權杖國王(King of Wands)逆位',"cardDes":'逆位的權杖國王可能暗示著控制欲、過度自信或領導風格的問題。在心理照護中，這張牌提醒人們要檢視自己的領導風格，並避免過度控制他人。'},
    
     {"cardName":'星幣一(Ace of Pentacles)正位',"cardDes":'正位的星幣一象徵著財富、機會和穩定。在心理照護中，這張牌鼓勵人們抓住財務和實際機會，並建立穩定的基礎。'},
    {"cardName":'星幣一(Ace of Pentacles)逆位',"cardDes":'逆位的星幣一可能意味著經濟困難、機會錯失或穩定性的問題。在心理照護中，這張牌提醒人們要檢視自己的財務狀況，並尋找改善的途徑。'},

    {"cardName":'星幣二(Two of Pentacles)正位',"cardDes":'正位的星幣二象徵著平衡、靈活和多重任務。在心理照護中，這張牌鼓勵人們在生活中找到平衡，並有效地管理多項責任。'},
    {"cardName":'星幣二(Two of Pentacles)逆位',"cardDes":'逆位的星幣二可能暗示著困難的平衡、時間管理問題或焦慮。在心理照護中，這張牌提醒人們要重新評估自己的工作和生活平衡，並尋求穩定。'},

    {"cardName":'星幣三(Three of Pentacles)正位',"cardDes":'正位的星幣三象徵著合作、技能和專業。在心理照護中，這張牌鼓勵人們尋求團隊合作，並發揮自己的專業技能來實現目標。'},
    {"cardName":'星幣三(Three of Pentacles)逆位',"cardDes":'逆位的星幣三可能意味著合作困難、缺乏專業或技能的問題。在心理照護中，這張牌提醒人們要解決與他人的合作問題，並提升自己的技能。'},

    {"cardName":'星幣四(Four of Pentacles)正位',"cardDes":'正位的星幣四象徵著穩定、安全和財務保護。在心理照護中，這張牌鼓勵人們重視經濟安全，並避免過度保守。'},
    {"cardName":'星幣四(Four of Pentacles)逆位',"cardDes":'逆位的星幣四可能暗示著財務不穩定、過度控制或情感封閉。在心理照護中，這張牌提醒人們要放下對物質的過度執著，並尋找情感上的平衡。'},

    {"cardName":'星幣五(Five of Pentacles)正位',"cardDes":'正位的星幣五象徵著困難、缺乏和失落。在心理照護中，這張牌提醒人們要面對財務或情感上的挑戰，並尋求支持和幫助。'},
    {"cardName":'星幣五(Five of Pentacles)逆位',"cardDes":'逆位的星幣五可能意味著恢復、改善財務狀況或從困境中走出。在心理照護中，這張牌鼓勵人們尋找解決困境的方法，並重建自己的生活。'},

    {"cardName":'星幣六(Six of Pentacles)正位',"cardDes":'正位的星幣六象徵著慷慨、平衡和公平。在心理照護中，這張牌鼓勵人們施以援手，並在接受幫助時保持謙遜。'},
    {"cardName":'星幣六(Six of Pentacles)逆位',"cardDes":'逆位的星幣六可能暗示著不公平、慷慨的困難或經濟上的不穩定。在心理照護中，這張牌提醒人們檢視自己的財務狀況，並平衡慷慨和自我保護。'},

    {"cardName":'星幣七(Seven of Pentacles)正位',"cardDes":'正位的星幣七象徵著耐心、等待和努力的成果。在心理照護中，這張牌鼓勵人們保持耐心，並相信自己的努力最終會帶來回報。'},
    {"cardName":'星幣七(Seven of Pentacles)逆位',"cardDes":'逆位的星幣七可能意味著失望、計劃的延遲或對成果的不滿。在心理照護中，這張牌提醒人們重新評估自己的目標，並調整策略以實現期望。'},

    {"cardName":'星幣八(Eight of Pentacles)正位',"cardDes":'正位的星幣八象徵著專注、技能和努力。在心理照護中，這張牌鼓勵人們致力於自我提升，並通過持續的努力達到專業和個人成就。'},
    {"cardName":'星幣八(Eight of Pentacles)逆位',"cardDes":'逆位的星幣八可能暗示著工作上的挑戰、缺乏動力或不滿意的成果。在心理照護中，這張牌提醒人們檢視自己的工作狀態，並尋求改善和激勵。'},

    {"cardName":'星幣九(Nine of Pentacles)正位',"cardDes":'正位的星幣九象徵著財富、獨立和成功。在心理照護中，這張牌鼓勵人們慶祝自己的成功，並享受生活中的豐富成果。'},
    {"cardName":'星幣九(Nine of Pentacles)逆位',"cardDes":'逆位的星幣九可能意味著對財富的依賴、孤立或安全感的缺失。在心理照護中，這張牌提醒人們檢視自己的生活方式，並尋找平衡和滿足感。'},

    {"cardName":'星幣十(Ten of Pentacles)正位',"cardDes":'正位的星幣十象徵著家庭、財富和長期的成功。在心理照護中，這張牌鼓勵人們重視家庭和長期的穩定，並建立持久的成功基礎。'},
    {"cardName":'星幣十(Ten of Pentacles)逆位',"cardDes":'逆位的星幣十可能暗示著家庭問題、財務困難或長期計劃的問題。在心理照護中，這張牌提醒人們要處理家庭和財務上的挑戰，並尋求支持。'},

    {"cardName":'星幣侍者(Page of Pentacles)正位',"cardDes":'正位的星幣侍者象徵著學習、實踐和新機會。在心理照護中，這張牌鼓勵人們追求學習和成長，並把握新機會。'},
    {"cardName":'星幣侍者(Page of Pentacles)逆位',"cardDes":'逆位的星幣侍者可能意味著學習的障礙、目標不清或實踐的困難。在心理照護中，這張牌提醒人們要重新評估自己的學習計劃，並尋找清晰的方向。'},

    {"cardName":'星幣騎士(Knight of Pentacles)正位',"cardDes":'正位的星幣騎士象徵著踏實、負責和穩定。在心理照護中，這張牌鼓勵人們以踏實的態度面對生活中的挑戰，並保持穩定的進展。'},
    {"cardName":'星幣騎士(Knight of Pentacles)逆位',"cardDes":'逆位的星幣騎士可能暗示著拖延、過度保守或缺乏進展。在心理照護中，這張牌提醒人們要克服拖延，並積極尋求進步。'},

    {"cardName":'星幣皇后(Queen of Pentacles)正位',"cardDes":'正位的星幣皇后象徵著實際、關愛和財務穩定。在心理照護中，這張牌鼓勵人們以關愛的態度對待自己和他人，並保持財務上的穩定。'},
    {"cardName":'星幣皇后(Queen of Pentacles)逆位',"cardDes":'逆位的星幣皇后可能意味著財務壓力、過度關注物質或情感冷漠。在心理照護中，這張牌提醒人們要平衡物質和情感，並關注內心的需求。'},

    {"cardName":'星幣國王(King of Pentacles)正位',"cardDes":'正位的星幣國王象徵著成功、實力和穩定。在心理照護中，這張牌強調財務成功和穩定的重要性，並鼓勵人們以成熟的態度面對生活中的挑戰。'},
    {"cardName":'星幣國王(King of Pentacles)逆位',"cardDes":'逆位的星幣國王可能暗示著財務問題、控制欲或缺乏穩定。在心理照護中，這張牌提醒人們要檢視自己的財務狀況，並避免過度控制或物質上的焦慮。'}
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
]

 
@app.route("/callback", methods=['POST'])
def callback():
    # Get X-Line-Signature from request header
    signature = request.headers['X-Line-Signature']

    # Get request body as text
    body = request.get_data(as_text=True)

    try:
        # Handle webhook body
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    # Return a 200 OK status code
    return 'OK', 200

def draw_card(category):
    card_dict = {
        '心理照護': care,
        '工作': work,
        '今日運勢': fortune,
        '愛情': love
    }
    if category not in card_dict:
        return '請輸入文字【工作】【愛情】【今日運勢】【心理照護】'
    
    selected_card = random.choice(card_dict[category])
    return f'抽到的是 {selected_card["cardName"]}， \n\n{selected_card["cardDes"]}'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=draw_card(event.message.text)) 
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)