from margining.initialMarginModel import InitialMarginModel


class NOIMM(InitialMarginModel):

    def get_im_post(self):
        return 0

    def get_im_receive(self):
        return 0