from rest_framework.views import APIView
from rest_framework.response import Response
import random

class PostProcView(APIView):

    def identity(self, options):
        out = []

        for opt in options:
            out.append({
                **opt,
                'postproc': opt['votes'],
            });

        out.sort(key=lambda x: -x['postproc'])
        return Response(out)


    def post(self, request):
        """
         * type: IDENTITY | EQUALITY | WEIGHT
         * options: [
            {
             option: str,
             number: int,
             votes: int,
             ...extraparams
            }
           ]
        """

        t = request.data.get('type', 'IDENTITY')
        opts = request.data.get('options', [])

        if t == 'IDENTITY':
            return self.identity(opts)
        elif t == 'WEIGHTED':
            return self.weightedOptions(opts)
        elif t=='RANDOM':
            return self.randomSelection(opts)
        elif t=='GENDER':
            return self.genderParity(opts)
        elif t=='BORDA':
            return self.borda_count(opts)
        elif t=='AGE':
            return self.ageLimit(opts)
        return Response({})
    #Each option has an assigned weight. The votes each option has received will be multiplied by their corresponding weight
    def weightedOptions(self, options):
        out = []

        for opt in options:
            out.append({
                **opt,
                'postproc': opt['votes']*opt['weight'],
            })

        out.sort(key=lambda x: -x['postproc'])
        return Response(out)

    #Only one option is chosen and returned. Options are chosen randomly, taking into account the percentage of votes each option got.
    def randomSelection(self, options):
        out = []
        totalVotes=0
        for opt in options:
            totalVotes+=opt['votes']

        for opt in options:
            out.append({
                **opt,
                'postproc': opt['votes'],
            })
        out.sort(key=lambda x: -x['postproc'])
        random.seed()
        randomNumber=random.randint(1,100)
        percentageAccumulated=0.0
        for o in out:
            if randomNumber-((o['votes']/totalVotes)*100+percentageAccumulated)<=0:
                chosen=o
                percentageAccumulated += (o['votes'] / totalVotes) * 100
                break
            percentageAccumulated+=(o['votes']/totalVotes)*100
        res=[]
        res.append({
                **chosen,
                'randomNumber': randomNumber,
                'percentageAccumulated':percentageAccumulated
            })
        return Response(res)


    # All options must be ordered and returned. Options are ordered according to gender parity
    def genderParity(self, options):
        out = []
        menList = []
        womenList = []

        for opt in options:
            if opt['gender'] == 'm':
                menList.append({
                    **opt,
                    'postproc': opt['votes']
                })
            elif opt['gender'] == 'w':
                womenList.append({
                    **opt,
                    'postproc': opt['votes']
                })
        menList.sort(key=lambda x: -x['postproc'])
        womenList.sort(key=lambda x: -x['postproc'])
        # limitar menList y womenList
        if len(menList) <= len(womenList):
            out = menList + womenList[:len(menList)]
        else:
            out = menList[:len(womenList)] + womenList

        out.sort(key=lambda x: -x['votes'])

        return Response(out)

    # Este metodo recibe los votos y devuelve los votos procesados según el algoritmo de recuento borda
    def borda_count(self,options):
        choices = options['choices']
        votes = options['votes']
        results = {}
        for i in choices:
            results[i] = 0

        for vote in votes:
            vote_len = len(vote)
            for option in vote:
                actual_vote_option = results[option]
                results[option] = actual_vote_option + (vote_len)
                vote_len -= 1

        return Response(results)

    # Limit results from options for age where minimum age is equals to 30 and maximum age is equals to 40
    def ageLimit(self, options):
        out = []
        minAge = 30
        maxAge = 40
        for opt in options:
            if minAge <= opt['age'] <= maxAge:
                out.append({**opt,
                            'postproc': minAge
                            })
        out.sort(key=lambda x: -x['age'], reverse=True)
        return Response(out)