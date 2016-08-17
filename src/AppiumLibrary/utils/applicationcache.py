from robot.utils import ConnectionCache
import robot

class ApplicationCache(ConnectionCache):

    def __init__(self):
        ConnectionCache.__init__(self, no_current_msg='No current application')
        self._closed = set()

    @property
    def applications(self):
        return self._connections

    def get_open_browsers(self):
        open_applications = []
        for application in self._connections:
            if application not in self._closed:
                open_applications.append(application)
        return open_applications

    def close(self):
        if self.current:
            application = self.current
            try:
                #robot.api.logger.debug('Executing close_app() in Appium WebDriver, session: %s' % application.session_id)
                #application.close_app()
                robot.api.logger.debug('Executing quit() in Appium WebDriver, session: %s' % application.session_id)
                application.quit()
            except Exception as ex:
                robot.api.logger.warn("Executing quit() in Appium WebDriver failed: '%s'" % str(ex))
                #robot.api.logger.warn("Executing close_app() in Appium WebDriver failed: '%s'" % str(ex))
            finally:
                self.current = self._no_current
                self.current_index = None
                self._closed.add(application)

    def close_all(self):
        for application in self._connections:
            if application not in self._closed:
                robot.api.logger.debug('Executing quit() in Appium WebDriver, session: %s' % application.session_id)
                try:
                    application.quit()
                except Exception as ex:
                    robot.api.logger.warn("Executing quit() in Appium WebDriver failed: '%s'" % str(ex))
        self.empty_cache()
        return self.current
