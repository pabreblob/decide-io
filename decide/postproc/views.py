from rest_framework.views import APIView
from rest_framework.response import Response
import random

class PostProcView(APIView):

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
        params = request.data.get('parameters', [])

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
        elif t=='HONDT':
            return self.hondt(opts)
        elif t=='AGE':
            return self.ageLimit(opts)
        elif t=='WEIGHTEDRANDOM':
            return self.weightedRandomSelection(opts)
        return Response({})

    def identity(self, options):
        out = []

        for opt in options:
            out.append({
                **opt,
                'postproc': opt['votes'],
            });

        out.sort(key=lambda x: -x['postproc'])
        return Response(out)

    #Each option has an assigned weight. The votes each option has received will be multiplied by their corresponding weight
    def weightedOptions(self, options):
        out = []

        for opt in options:
            out.append({
                **opt,
                'postproc': opt['votes']*opt['weight'],
            })

        out.sort(key=lambda x: x['postproc'])
        return Response(out)

    #Only one option is chosen and returned. Options are chosen randomly, taking into account the percentage of votes each option got.
    def randomSelection(self, options):
        out = []
        totalVotes=0

        for opt in options:
            out.append({
                **opt,
                'postproc': opt['votes'],
            })
            totalVotes += opt['votes']

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

        #Here we are going to implement d'Hont Method (CarlosC)
        # quot = TotalNumberOfVotes / (SeatsOfParty + 1)
        #initially SeatsOfParty = 0 for all parties
    def hondt(self, options):
            escanos = options['escanos']
            votos = options['votes']

            aux2 = escanos

            for i in votos:
                i['seat'] = 0

            for i in range(0, escanos):
                maximum = [None, 0]
            for x in votos:
                voto_actual = x['votes']
                formula_aplicada = voto_actual / (x['seat'] + 1)
                if formula_aplicada > maximum[1]:
                    maximum = [x['option'], formula_aplicada]
            for g in votos:
                if g['option'] == maximum[0]:
                    g['seat'] += 1
            aux2 -= 1
            return Response(votos)



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

    # This method receives the number of votes (as points) each choice had.
    # Given n the number of choices, each voter rank the n choices
    # by his/her preference.
    # Given the rank each choice has to a voter, different points are assigned
    # being 1 the minimum and n the maximum.
    def borda_count(self,options):
        out = []

        for opt in options:
            out.append({
                **opt,
                'postproc': round(opt['votes']/len(options), 5 ),
            })

        out.sort(key=lambda x: -x['postproc'])

        return Response(out)

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
    #Only one option is chosen and returned. Options are chosen randomly, taking into account the percentage of votes
    # ach option got multiplied by its weight.
    def weightedRandomSelection(self, options):
        out = []
        totalPoints=0
        for opt in options:
            out.append({
                **opt,
                'postproc': opt['votes']*opt['weight'],
            })
            totalPoints += opt['votes'] * opt['weight']
        out.sort(key=lambda x: -x['postproc'])
        random.seed()
        randomNumber=random.randint(1,100)
        percentageAccumulated=0.0
        for o in out:
            if randomNumber-((o['votes']*o['weight']/totalPoints)*100+percentageAccumulated)<=0:
                chosen=o
                percentageAccumulated += (o['votes']*o['weight'] / totalPoints) * 100
                break
            percentageAccumulated+=(o['votes']*o['weight']/totalPoints)*100
        res=[]
        res.append({
                **chosen,
                'randomNumber': randomNumber,
                'percentageAccumulated':percentageAccumulated
            })
        return Response(res)
