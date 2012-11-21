from consumer import Consumer, DefaultEnvironment
import util

class Wizard(object):
    def __init__(self, endpoint, environment = None):
        super(Wizard, self).__init__()
        self.endpoint    = endpoint
        self.file_hint   = None
        self.environment = environment
        if not self.environment: self.environment = DefaultEnvironment()

        try:
            self.payload   = self.environment.json(util.sources_endpoint(self.endpoint))
            self.file_hint = self.payload['title']
        except: pass

    def filtered_sources(self):
        filtered = []

        try:
            sources  = self.payload.get('items', [])
            filtered = filter(lambda x: x['_type'] == 'foreign', sources)
        except: pass

        return filtered

    def translate(self, foreign):
        response = self.environment.json( util.translate_endpoint( foreign['original_url'], foreign['foreign_url'] ) )
        return util.translated_from(response)

    #def sources(self):
        #for foreign in self.filtered_sources():
            #try:
                #consumer = Consumer(self.translate(foreign), environment = self.environment)
                #consumer.consume()
                #yield consumer
                #break
            #except GeneratorExit:
                #pass
            #except Exception, e:
                #util.print_exception(e)
                #continue

    def sources(self, cb):
        for foreign in self.filtered_sources():
            try:
                consumer = Consumer(self.translate(foreign), environment = self.environment)
                cb(consumer)
                break
            except Exception, e:
                continue

if __name__ == '__main__':
    import os, sys
    args     = sys.argv
    test_url = args[1]

    found = None
    def test():
        w = Wizard(test_url)
        print w.file_hint

        def print_url(c):
            global found
            found = c.asset_url()

        w.sources(print_url)
        print found

    test()