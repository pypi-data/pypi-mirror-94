from pyrez.models import APIResponse
from pyrez.models.Mixin import MatchId
class TopMatch(APIResponse, MatchId):
    def __init__(self, **kwargs):
        APIResponse.__init__(self, **kwargs)
        MatchId.__init__(self, **kwargs)
        self.ban1Id = kwargs.get("Ban1Id", 0) or 0
        self.ban1Name = kwargs.get("Ban1", '') or ''
        self.ban2Id = kwargs.get("Ban2Id", 0) or 0
        self.ban2Name = kwargs.get("Ban2", '') or ''
        self.entryDatetime = kwargs.get("Entry_Datetime", '') or ''
        self.liveSpectators = kwargs.get("LiveSpectators", 0) or 0
        self.matchTime = kwargs.get("Match_Time", 0) or 0
        self.offlineSpectators = kwargs.get("OfflineSpectators", 0) or 0
        self.queueName = kwargs.get("Queue", '') or ''
        self.recordingFinished = kwargs.get("RecordingFinished", '') or ''
        self.recordingStarted = kwargs.get("RecordingStarted", '') or ''
        self.team1AvgLevel = kwargs.get("Team1_AvgLevel", 0) or 0
        self.team1Gold = kwargs.get("Team1_Gold", 0) or 0
        self.team1Kills = kwargs.get("Team1_Kills", 0) or 0
        self.team1Score = kwargs.get("Team1_Score", 0) or 0
        self.team2AvgLevel = kwargs.get("Team2_AvgLevel", 0) or 0
        self.team2Gold = kwargs.get("Team2_Gold", 0) or 0
        self.team2Kills = kwargs.get("Team2_Kills", 0) or 0
        self.team2Score = kwargs.get("Team2_Score", 0) or 0
        self.winningTeam = kwargs.get("WinningTeam", 0) or 0
