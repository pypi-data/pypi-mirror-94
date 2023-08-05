from enum import IntEnum

import socket


class ServerDisconnectedException(Exception):
    """
    ServerDisconnectedException is raised when the connection with server was lost.
    :param message: Exception message.
    """

    def __init__(self, message=__doc__):
        self.message = message
        super().__init__(self.message)


class ValueOutOfRangeException(Exception):
    """
    ValueOutOfRangeException is raised when given parameter value is out of range.
    :param message: Exception message.
    """

    def __init__(self, message=__doc__):
        self.message = message
        super().__init__(self.message)


class RelayAction(IntEnum):
    """Possible relay actions."""
    MOMENTARY_ACTIVATION = 1
    LATCH = 2
    RELEASE = 3
    INQUIRY = 9


class OptoAction(IntEnum):
    """Possible opto actions."""
    OFF = 0
    ON = 1
    INQUIRY = 9


class SalvoOption(IntEnum):
    """Describes how salvos are organized."""
    ACTUAL_SALVO_NUM = 1
    ALPHANUMERIC_POSITION_OF_SALVO = 2


class CrosspointTransitionControlSetting(IntEnum):
    """Possible transition control settings."""
    CUT_OUT_CUT_IN = 0
    CUT_OUT_FADE_IN = 1
    FADE_OUT_CUT_IN = 2
    FADE_OUT_FADE_IN = 3
    CROSS_FADE = 4
    CUT_OUT_CUT_IN_WITH_DSP = 9


class FadeTime(IntEnum):
    """Possible fade times."""
    INSTANT = 0
    T_10MS = 1
    T_50MS = 2
    T_100MS = 3
    T_200MS = 4
    T_500MS = 5
    T_1S = 6
    T_2S = 7
    T_3S = 8
    T_4S = 9
    T_5S = 10
    T_6S = 11
    T_7S = 12
    T_8S = 13
    T_9S = 14
    T_10S = 15


class GainChangeStage(IntEnum):
    """Possible gain change stages."""
    SOURCE_INPUT_SENSITIVITY = 1
    OUTPUT_GAIN_TRIM = 3
    DSP_COEFFICIENT_LEVEL_NO_FADE_TIME = 10
    DSP_COEFFICIENT_LEVEL_FADE_TIME = 11
    DSP_MIXER_OUTPUT_MASTER_LEVEL_NO_FADE_TIME = 15
    DSP_MIXER_OUTPUT_MASTER_LEVEL_FADE_TIME = 16


class StereoLinkOption(IntEnum):
    """Describes if input or output should be modified."""
    INPUT_LINK = 0
    OUTPUT_LINK = 1


class StereoLinkSetting(IntEnum):
    """Types of inputs and outputs."""
    MONO = 0
    STEREO = 1
    SOURCE_DEPENDENT = 2
    LR_MONO_SUM = 3


class EnhancedTakeOptions:
    """Describes arguments for enhancement_take() method."""

    class PriorityLevel(IntEnum):
        """Possible priority levels."""
        STANDARD = 0
        IFB = 1

    class ControlOptions(IntEnum):
        """Possible control options."""
        OFF = 0
        ON = 1
        MOMENTARY = 2

    class ActionOptions(IntEnum):
        """Possible actions."""
        TAKE = 0
        SUM = 1
        DIRECT_RELAY_CONTROL = 2

    class SuppliedGainValueUsage(IntEnum):
        """Should use specified gain value."""
        NO = 0
        YES = 1

    class CurrentXpointTransitionCtlSpec(IntEnum):
        """Should use current xpoint transition control specification."""
        NO = 0
        YES = 1

    def __init__(self,
                 priority_level: PriorityLevel,
                 control_options: ControlOptions,
                 action_options: ActionOptions,
                 use_supplied_gain_value: SuppliedGainValueUsage,
                 use_current_xpoint_transition_ctl_spec: CurrentXpointTransitionCtlSpec
                 ):
        self.value = int(priority_level)
        self.value += int(control_options) << 2
        self.value += int(action_options) << 5
        self.value += int(use_supplied_gain_value) << 9
        self.value += int(use_current_xpoint_transition_ctl_spec) << 10

    def get(self):
        """
        Get calculated enhanced take command options numeric value.
        :return: value calculated for arguments provided in constructor.
        """
        return self.value


class ConsoleModuleAction(IntEnum):
    """Possible console module actions."""
    TURN_MODULE_OFF_WITH_SOURCE_SELECTED = 0
    TURN_MODULE_ON_WITH_SOURCE_SELECTED = 1
    TURN_CUE_OFF_ON_MODULE_WITH_SOURCE_SELECTED = 2
    TURN_CUE_ON_ON_MODULE_WITH_SOURCE_SELECTED = 3


class AlphanumericNameInquiryInputOutput(IntEnum):
    """Alphanumeric name inquiry should be shown for input or output."""
    INPUT = 0
    OUTPUT = 1


class FeedbackReplies(IntEnum):
    """Feedback replies should be enabled or disabled."""
    ENABLED = 1
    DISABLED = 0


class FeedbackTally(IntEnum):
    """Possible feedback tally options."""
    NO_TALLY_OF_XPOINT_ACTIVITY_OR_ALPHA_CHANGE_NOTIFICATION = 0
    XPOINT_TALLY_IN_NUMERICAL_FORMAT_ONLY = 1
    XPOINT_TALLY_AS_CHANNEL_ALPHA_LABELS_ONLY = 2
    XPOINT_TALLY_BOTH_NUMERICAL_AND_ALPHA_LABELS = 3
    NOTIFICATION_OF_CHANGES_TO_THE_ALPHA_LABELS = 4
    NUMERICAL_TALLY_AND_ALPHA_CHANGE_NOTIFICATION = 5
    ALPHA_LABEL_TALLY_AND_ALPHA_CHANGE_NOTIFICATION = 6
    NUMERICAL_AND_ALPHA_LABEL_TALLY_WITH_ALPHA_CHANGE_NOTICE = 7
    NOTICE_OF_CONSOLE_MODULE_OPERATIONS_ONLY = 8
    NOTICE_OF_CONSOLE_MODULE_OPERATIONS_AND_NUMERICAL_TALLY_AND_ALPHA_CHANGE_NOTIFICATION = 9


class FeedbackProtocol(IntEnum):
    """Possible feedback variants."""
    THREE_DIGIT_ASCII_STYLE_XPOINT_TALLY = 0
    TWO_DIGIT_ASCII_HEX_STYLE_XPOINT_TALLY = 1
    FOUR_DIGIT_ASCII_STYLE_XPOINT_TALLY = 2


class Reply(IntEnum):
    """Default replies."""
    OK = 0
    ERROR = 1


def reply_from_str(s: str):
    """
    Function which converts string replies to Reply class types.
    :param s: string to convert
    :return: Reply.OK or Reply.ERROR
    """
    if "OK" in s:
        return Reply.OK
    else:
        return Reply.ERROR


class Sas32kd:
    """
    Defines methods to manage SAS 32KD audio router.
    """

    def __init__(self, ip, port=1270, timeout=5):
        """
        Constructor.
        :param ip: IP address of TCP/IP server module.
        :param port: Port of TCP/IP server module.
        :param timeout: Connection timeout.
        """
        self.is_disconnected = True
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(timeout)
        self.s.connect((ip, port))
        self.s.recv(64)
        self.is_disconnected = False

    def disconnect(self):
        """
        Disconnects from TCP/IP server module.
        """
        self.is_disconnected = True
        self.s.close()

    def take(self, inp: int, outp: int):
        """
        Standard take command.
        :param inp: Input channel number
        :param outp: Output channel number
        :return: OK or ERROR
        """
        if not self.is_disconnected:
            if inp < 1 or inp > 999:
                raise ValueOutOfRangeException("inp must be >= 1 and <= 999")
            if outp < 1 or outp > 999:
                raise ValueOutOfRangeException("outp must be >= 1 and <= 999")
            inp_str = str(inp).zfill(3)
            outp_str = str(outp).zfill(3)
            self.s.sendall(bytes('\x14' + inp_str + outp_str, encoding='utf8'))
            return reply_from_str(self.s.recv(64).decode())
        else:
            raise ServerDisconnectedException

    def relay(self, action: RelayAction, num: int):
        """
        Reply command.
        :param action: Action to be performed on relay.
        :param num: Relay number.
        :return: OK or ERROR
        """
        if not self.is_disconnected:
            if num < 1 or num > 999:
                raise ValueOutOfRangeException("num must be >= 1 and <= 999")
            n_str = str(num).zfill(3)
            act_str = str(int(action))
            self.s.sendall(bytes('\x12' + act_str + n_str, encoding='utf8'))
            return reply_from_str(self.s.recv(64).decode())
        else:
            raise ServerDisconnectedException

    def opto(self, action: OptoAction, num: int):
        """
        Opto command.
        :param action: Action to be performed on opto.
        :param num: Opto number.
        :return: OK or ERROR
        """
        if not self.is_disconnected:
            if num < 1 or num > 999:
                raise ValueOutOfRangeException("num must be >=1 and <= 999")
            n_str = str(num).zfill(3)
            act_str = str(int(action))
            self.s.sendall(bytes('\x0F' + act_str + n_str, encoding='utf8'))
            return reply_from_str(self.s.recv(64).decode())
        else:
            raise ServerDisconnectedException

    def salvo(self, option: SalvoOption, num: int):
        """
        Salvo command.
        :param option: Ordering type of salvos.
        :param num: Salvo number.
        :return: OK or ERROR.
        """
        if not self.is_disconnected:
            if num < 1 or num > 256:
                raise ValueOutOfRangeException("num must be >=1 and <= 256")
            n_str = str(num).zfill(3)
            act_str = str(int(option))
            self.s.sendall(bytes('\x13' + act_str + n_str, encoding='utf8'))
            return reply_from_str(self.s.recv(64).decode())
        else:
            raise ServerDisconnectedException

    def crosspoint_transition_control(self, setting: CrosspointTransitionControlSetting,
                                      fade_in_time: FadeTime, fade_out_time: FadeTime, channel: int):
        """
        Crosspoint transition control.
        :param setting: Type of transition.
        :param fade_in_time: Fade in time. (Refer: FadeTime class).
        :param fade_out_time: Fade out time. (Refer: FadeTime class).
        :param channel: Output channel number.
        :return: OK or ERROR
        """
        if not self.is_disconnected:
            if channel < 1 or channel > 9997:
                raise ValueOutOfRangeException("num must be >=1 and <= 9997")
            channel_str = str(channel).zfill(4)
            setting_str = str(int(setting)).zfill(2)
            fade_in_str = str(int(fade_in_time)).zfill(2)
            fade_out_str = str(int(fade_out_time)).zfill(2)
            self.s.sendall(bytes('\x11' + setting_str + fade_in_str +
                                 fade_out_str + channel_str, encoding='utf8'))
            return reply_from_str(self.s.recv(64).decode())
        else:
            raise ServerDisconnectedException

    def gain_change(self, inp: int, outp: int, gain: int, fade_time: FadeTime, stage: GainChangeStage):
        """
        Gain change command.
        :param inp: Input channel number.
        :param outp: Output channel number.
        :param gain: Source target gain level (1/10 dB steps, 1024 = Unity; valid 0 to 2048).
        :param fade_time: Fade time. (Refer: FadeTime class).
        :param stage: Gain change stage.
        :return: OK or ERROR.
        """
        if not self.is_disconnected:
            if inp < 1 or inp > 9999:
                raise ValueOutOfRangeException("inp must be >=1 and <= 9999")
            if outp < 1 or outp > 9999:
                raise ValueOutOfRangeException("outp must be >=1 and <= 9999")
            if gain < 0 or gain > 2048:
                raise ValueOutOfRangeException(
                    "gain must be >=0 and <= 2048. 1024 = unity. step = 1/10 dB")
            inp_str = str(inp).zfill(4)
            outp_str = str(outp).zfill(4)
            gain_str = str(gain).zfill(4)
            fade_time_str = str(int(fade_time)).zfill(2)
            stage_str = str(int(stage)).zfill(2)
            self.s.sendall(bytes('\x1A10' + inp_str + outp_str +
                                 gain_str + fade_time_str + stage_str, encoding='utf8'))
            return reply_from_str(self.s.recv(64).decode())
        else:
            raise ServerDisconnectedException

    def stereo_link(self, option: StereoLinkOption, setting: StereoLinkSetting, channel: int):
        """
        Stereo link modifier.
        :param option: Input or output link.
        :param setting: Mono, stereo, source dependent or LR mono sum. (Refer: StereoLinkSetting class).
        :param channel: Output channel number.
        :return: OK or ERROR.
        """
        if not self.is_disconnected:
            if channel < 1 or channel > 9997:
                raise ValueOutOfRangeException(
                    "channel must be >=1 and <= 9997")
            channel_str = str(channel).zfill(4)
            option_str = str(int(option))
            setting_str = str(int(setting)).zfill(2)
            self.s.sendall(bytes('\x0C' + option_str +
                                 setting_str + channel_str, encoding='utf8'))
            return reply_from_str(self.s.recv(64).decode())
        else:
            raise ServerDisconnectedException

    def enhanced_take(self, inp: int, outp: int, gain: int, options: EnhancedTakeOptions):
        """
        Enhanced take command.
        :param inp: Input channel number.
        :param outp: Output channel number.
        :param gain: Source target gain level (1/10 dB steps, 1024 = Unity; valid 0 to 2048).
        :param options: Options. (Refer: EnhancedTakeOptions class).
        :return: OK or ERROR.
        """
        if not self.is_disconnected:
            if inp < 1 or inp > 9999:
                raise ValueOutOfRangeException("inp must be >=1 and <= 9999")
            if outp < 1 or outp > 9999:
                raise ValueOutOfRangeException("outp must be >=1 and <= 9999")
            if gain < 0 or gain > 2048:
                raise ValueOutOfRangeException(
                    "gain must be >=0 and <= 2048. 1024 = unity. step = 1/10 dB")
            inp_str = str(inp).zfill(4)
            outp_str = str(outp).zfill(4)
            gain_str = str(gain).zfill(4)
            options_str = str(options.get()).zfill(5)
            self.s.sendall(bytes('\x1A00' + inp_str + outp_str +
                                 gain_str + options_str, encoding='utf8'))
            return reply_from_str(self.s.recv(64).decode())
        else:
            raise ServerDisconnectedException

    def console_module_control(self, action: ConsoleModuleAction, console_id: int, source: int):
        """
        Console module control commands.
        :param action: Console source/module control options. (Refer: ConsoleModuleAction class).
        :param console_id: System console number (1 to 256 or 999 = any).
        :param source: Source channel number (1 to 9998).
        :return: OK or ERROR.
        """
        if not self.is_disconnected:
            if console_id < 1 or (console_id > 256 and console_id != 999):
                raise ValueOutOfRangeException(
                    "console_id must be (>=1 and <= 256) or =999 (any console)")
            if source < 1 or source > 9998:
                raise ValueOutOfRangeException(
                    "source must be >=1 and <= 9998")
            action_str = str(int(action))
            console_id_str = str(console_id).zfill(3)
            source_str = str(source).zfill(4)
            self.s.sendall(bytes('\x1A20' + action_str +
                                 console_id_str + source_str, encoding='utf8'))
            return reply_from_str(self.s.recv(64).decode())
        else:
            raise ServerDisconnectedException

    def console_module_channel_label_override(self, console_id: int, source: int, label: str):
        """
        Console module channel label override command.
        :param console_id: System console number (1 to 256 or 999 = any).
        :param source: Source channel number (1 to 9998).
        :param label: 8 character alpha label to be displayed by the addressed modules.
        :return: OK or ERROR.
        """
        if not self.is_disconnected:
            if console_id < 1 or (console_id > 256 and console_id != 999):
                raise ValueOutOfRangeException(
                    "console_id must be (>=1 and <= 256) or =999 (any console)")
            if source < 1 or source > 9998:
                raise ValueOutOfRangeException(
                    "source must be >=1 and <= 9998")
            if len(label) > 8:
                label = label[0:8]
            console_id_str = str(console_id).zfill(3)
            source_str = str(source).zfill(4)
            self.s.sendall(bytes('\x1A21' + console_id_str +
                                 source_str + label, encoding='utf8'))
            return reply_from_str(self.s.recv(64).decode())
        else:
            raise ServerDisconnectedException

    def inquiry(self, outp: int):
        """
        Inquiry command (xpoint state).
        :param outp: Output channel (1 to 256 or 999 - any).
        :return: Three digit input assigned to specified output or inputs assigned to each output in ascending order.
        """
        if not self.is_disconnected:
            if outp < 1 or (outp > 256 and outp != 999):
                raise ValueOutOfRangeException(
                    "outp must be (>=1 and <= 256) or =999 (any console)")
            outp_str = str(outp).zfill(3)
            self.s.sendall(bytes('\x09' + outp_str, encoding='utf8'))
            if outp == 999:
                ret = self.s.recv(100000).decode().split(' ')
                ret2 = ret.pop(255)
                ret2 = ret2.split('\r\n')
                return ret + ret2
            else:
                return int(self.s.recv(64).decode())
        else:
            raise ServerDisconnectedException

    def expanded_channel_inquiry(self, destination: int):
        """
        Expanded channel inquiry (multiple sources).
        :param destination: Destination channel number (1 to 9998).
        :return: Dict with all sources currently assigned to output, with priority levels.
        """
        if not self.is_disconnected:
            if destination < 1 or destination > 9998:
                raise ValueOutOfRangeException(
                    "destination must be >=1 and <= 9998")
            destination_str = str(int(destination)).zfill(4)
            self.s.sendall(bytes('\x1A50' + destination_str, encoding='utf8'))
            try:
                res = self.s.recv(1024).decode()[:-2]
                res = res.split(':')
                return {
                    'output': int(res[0][1:]),
                    'priority_level': int(res[1][1:]),
                    'inputs': [int(x) for x in res[3].split(',') if x != '']
                }
            except Exception:
                return Reply.ERROR
        else:
            raise ServerDisconnectedException

    def alphanumeric_name_inquiry(self, input_output: AlphanumericNameInquiryInputOutput, channel_num: int):
        """
        Alphanumeric name inquiry command.
        To obtain the alphanumeric names which have been programmed to sources and destinations.
        :param input_output: Input or output. (Refer: AlphanumericNameInquiryInputOutput class).
        :param channel_num: Channel number.
            (1 to 256. 998 - all channel sorted alphabetically. 999 - all channels in order of channel number).
        :return: Alpha label for input or output.
        """
        if not self.is_disconnected:
            if channel_num < 1 or (channel_num > 256 and channel_num != 999 and channel_num != 998):
                raise ValueOutOfRangeException(
                    "channel_num must be (>=1 and <= 256) "
                    "or =999 (all channels in order of channel number) "
                    "or =998 (all channels sorted alphabetically"
                )
            channel_num_str = str(int(channel_num)).zfill(3)
            if input_output == AlphanumericNameInquiryInputOutput.INPUT:
                self.s.sendall(
                    bytes('\x18' + channel_num_str, encoding='utf8'))
                ret = self.s.recv(64000)
                try:
                    ret = ret.decode()
                except UnicodeDecodeError:
                    ret = str(ret[2:-1].decode())
                finally:
                    return ret
            elif input_output == AlphanumericNameInquiryInputOutput.OUTPUT:
                self.s.sendall(
                    bytes('\x19' + channel_num_str, encoding='utf8'))
                ret = self.s.recv(64000)
                try:
                    ret = ret.decode()
                except UnicodeDecodeError:
                    ret = str(ret[2:-1].decode())
                finally:
                    return ret
            else:
                return Reply.ERROR
        else:
            raise ServerDisconnectedException

    def feedback(self, replies: FeedbackReplies, feedback_tally: FeedbackTally, feedback_protocol: FeedbackProtocol):
        """
        Feedback command.
        Controls the system responses which will be output from the serial interface.
        :param replies: Enable or disable replies. (Refer: FeedbackReplies class).
        :param feedback_tally: Feedback tally variants. (Refer: FeedbackTally class).
        :param feedback_protocol: Feedback protocol variants. (Refer: FeedbackProtocol class).
        :return: OK or ERROR.
        """
        if not self.is_disconnected:
            replies_str = str(int(replies))
            feedback_tally_str = str(int(feedback_tally))
            feedback_protocol_str = str(int(feedback_protocol))
            self.s.sendall(bytes(
                '\x06' + replies_str + feedback_tally_str + feedback_protocol_str, encoding='utf8'))
            return reply_from_str(self.s.recv(64).decode())
        else:
            raise ServerDisconnectedException


class Sas32kdListener:
    """
    A class to simplify performing tasks when a specific event occurs.
    """

    def __init__(self, ip, port=1270):
        """
        Constructor.
        :param ip: IP address of TCP/IP server module.
        :param port: Port of TCP/IP server module.
        """
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((ip, port))
        self.s.setblocking(True)
        self.s.recv(64)
        self.codes = []

    def disconnect(self):
        """
        Disconnects from server.
        """
        self.s.close()

    def on_opto_turned_on(self, opto_num: int, func, *args, **kwargs):
        """
        Method to attach user function which will be performed after a specified opto will turn on.
        :param opto_num: Opto number.
        :param func: Function.
        :param args: Function args.
        :param kwargs: Function kwargs.
        """
        d = {
            'code': "Z00:" + str(opto_num).zfill(4) + ":1",
            'func': func,
            'args': args,
            'kwargs': kwargs
        }
        self.codes.append(d)

    def on_opto_turned_off(self, opto_num: int, func, *args, **kwargs):
        """
        Method to attach user function which will be performed after a specified opto will turn off.
        :param opto_num: Opto number.
        :param func: Function.
        :param args: Function args.
        :param kwargs: Function kwargs.
        """
        d = {
            'code': "Z00:" + str(opto_num).zfill(4) + ":0",
            'func': func,
            'args': args,
            'kwargs': kwargs
        }
        self.codes.append(d)

    def on_relay_turned_on(self, relay_num: int, func, *args, **kwargs):
        """
        Method to attach user function which will be performed after a specified relay will turn on.
        :param relay_num: Opto number.
        :param func: Function.
        :param args: Function args.
        :param kwargs: Function kwargs.
        """
        d = {
            'code': "Z01:" + str(relay_num).zfill(4) + ":1",
            'func': func,
            'args': args,
            'kwargs': kwargs
        }
        self.codes.append(d)

    def on_relay_turned_off(self, relay_num: int, func, *args, **kwargs):
        """
        Method to attach user function which will be performed after a specified relay will turn off.
        :param relay_num: Opto number.
        :param func: Function.
        :param args: Function args.
        :param kwargs: Function kwargs.
        """
        d = {
            'code': "Z01:" + str(relay_num).zfill(4) + ":0",
            'func': func,
            'args': args,
            'kwargs': kwargs
        }
        self.codes.append(d)

    def on_take(self, inp: int, outp: int, func, *args, **kwargs):
        """
        Method to attach user function which will be performed after specified input will be taken by specified output.
        :param inp: Input number.
        :param outp: Output number.
        :param func: Function.
        :param args: Function args.
        :param kwargs: Function kwargs.
        """
        d = {
            'code': "T" + str(inp).zfill(3) + ":" + str(outp).zfill(3),
            'func': func,
            'args': args,
            'kwargs': kwargs
        }
        self.codes.append(d)

    def run(self):
        """
        Listens for events.
        """
        while True:
            ret = self.s.recv(64)
            for c in self.codes:
                if bytes(c['code'], 'utf-8') in ret:
                    c['func'](*c['args'], **c['kwargs'])
