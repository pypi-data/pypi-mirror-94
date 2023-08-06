from opentrons import types
import pkg_resources
import json
import subprocess

metadata = {
    'protocolName': 'Miniaturized Quick-DNA/RNA™ Viral MagBead',
    'author': 'Per Adastra <adastra.aspera.per@gmail.com>',
    'apiLevel': '2.9'
}

# todo: Put these vars into a class which can be in a seperate file
trash_start_int = 0
left_side = 1
magbead_elution_volume = 13
right_side = -1
number_of_samples = 48
prok_control_mix_reps = 10
prok_incubation_time_in_minutes = 15
magbead_binding_time_in_minutes = 3
magbead_buffer_mix_reps = 30
mix_prok_into_sample_reps = 10
wash_buffer_reps = 5
# todo check dispense depth
dispense_depth = 5
extraction_elution_bind_time_in_minutes = 2
ethanol_dry_time_in_minutes = 5
starting_sample_volume = 60

left_column_names = "A1",  # "A2", "A3", "A4", "A5", "A6"
right_column_names = "A7",  # "A8", "A9", "A10", "A11", "A12"
poz_neg_sequence = -1,  # 1 , -1 , 1, -1 , 1
side = dict(zip((left_column_names + right_column_names), (poz_neg_sequence * 2)))


def run(protocol):

    def play_alert_sound(sound):
        AUDIO_FILE_PATH = pkg_resources.resource_filename('aidenbots', 'sounds/' + sound)
        subprocess.run(['mpg123', AUDIO_FILE_PATH], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def import_custom_labware(custom_labware_file_name):
        labware_file = pkg_resources.resource_filename('aidenbots', 'labware/' + custom_labware_file_name + '.json')
        with open(labware_file) as labware_def:
            data = json.load(labware_def)
        return data

    # import custom labware
    eppendorf_96_well_lobind_plate_500ul = import_custom_labware("eppendorf_96_well_lobind_plate_500ul")

    # tips
    p300_box1 = protocol.load_labware('opentrons_96_filtertiprack_200ul', '2')
    p20_box1 = protocol.load_labware('opentrons_96_filtertiprack_20ul', '6')

    # pipette hardware
    p300 = protocol.load_instrument('p300_multi_gen2', 'right')
    p20 = protocol.load_instrument('p20_multi_gen2', 'left')

    # modules
    magnetic_module = protocol.load_module('magnetic module gen2', '4')

    # plates & reservoir
    rt_wells = protocol.load_labware('usascientific_12_reservoir_22ml', '3')
    lb_plt = magnetic_module.load_labware_from_definition(eppendorf_96_well_lobind_plate_500ul)

    # trash Box
    trash_bin = protocol.fixed_trash['A1']

    # rt reagents
    nna_lysis_buffer_beads = rt_wells['A1']
    magbead_nna_wash_1 = rt_wells['A2']
    magbead_nna_wash_2 = rt_wells['A3']
    ethanol_1 = rt_wells['A4']
    nf_water = rt_wells['A5']

    def magnetic_module_engage(time_in_minutes=0.0, heightin_mm=0.0):
        magnetic_module.engage(heightin_mm)
        protocol.delay(minutes=time_in_minutes)

    def set_speed_profile(instrument, new_aspirate_speed, new_dispense_speed):
        instrument.flow_rate.aspirate = new_aspirate_speed
        instrument.flow_rate.dispense = new_dispense_speed

    def flash(reps=10):
        for _ in range(reps):
            for bol in (False, True):
                protocol.set_rail_lights(bol)
                protocol.delay(seconds=0.10)

    def aspirate_reagent(instrument, volume, reagent):
        instrument.aspirate(volume, reagent.bottom(1))
        protocol.delay(seconds=1)
        protocol.max_speeds['Z'] = protocol.max_speeds['A'] = 20
        instrument.move_to(reagent.top())
        protocol.max_speeds['Z'] = protocol.max_speeds['A'] = None

    def side_dispense(instrument, volume, location):
        instrument.flow_rate.dispense = 30
        instrument.move_to(location.top(-3))
        instrument.dispense(volume, location.top(-3).move(types.Point(y=2.25)))
        protocol.delay(seconds=1)
        instrument.flow_rate.blow_out = 30
        instrument.blow_out(location.top(-3).move(types.Point(y=2.25)))
        protocol.delay(seconds=1)
        instrument.move_to(location.top(-3))

    def exit_well(instrument, well):
        instrument.move_to(well.bottom(5))
        protocol.max_speeds['Z'] = protocol.max_speeds['A'] = 20
        instrument.move_to(well.bottom(10))
        protocol.max_speeds['Z'] = protocol.max_speeds['A'] = None

    def trash_tip(instrument):
        instrument.drop_tip()

    def extraction_plate_well_wash(sc):
        p300.move_to(lb_plt[sc].top(-3))
        p300.dispense(50, lb_plt[sc].top().move(types.Point(x=-3.2, y=0, z=-3)))
        p300.dispense(50, lb_plt[sc].top().move(types.Point(x=+3.2, y=0, z=-3)))
        p300.dispense(50, lb_plt[sc].top().move(types.Point(x=0, y=+3.2, z=-3)))
        p300.dispense(50, lb_plt[sc].top().move(types.Point(x=0, y=-3.2, z=-3)))
        p300.move_to(lb_plt[sc].top(-3))

    def remove_bead_wash_buffer(volume, sc):
        p300.flow_rate.aspirate = 5
        for _ in range(3):
            p300.aspirate((volume / 3), lb_plt[sc].bottom(0.5).move(types.Point(x=2 * int(side[sc]))))
            protocol.delay(seconds=3)

    def elute_na_from_beads(sc, volume=20):
        set_speed_profile(p300, 200, 50)
        p300.move_to(lb_plt[sc].bottom().move(types.Point(z=5)))
        p300.dispense(20, lb_plt[sc].bottom().move(types.Point(x=-2 * int(side[sc]), y=0, z=5)))
        p300.blow_out(lb_plt[sc].bottom().move(types.Point(x=-2 * int(side[sc]), y=0, z=5)))
        for _ in range(5):
            p300.aspirate(volume, lb_plt[sc].bottom(0.5))
            p300.dispense(volume, lb_plt[sc].bottom().move(types.Point(x=-2 * int(side[sc]), y=1.5, z=5)))
            p300.aspirate(volume, lb_plt[sc].bottom())
            p300.dispense(volume, lb_plt[sc].bottom().move(types.Point(x=-2 * int(side[sc]), y=0, z=5)))
            p300.aspirate(volume, lb_plt[sc].bottom())
            p300.dispense(volume, lb_plt[sc].bottom().move(types.Point(x=-2 * int(side[sc]), y=-1.5, z=5)))
        set_speed_profile(p300, 200, 200)
        p300.mix(10, volume * (3 / 4), lb_plt[sc].bottom())
        p300.blow_out(lb_plt[sc].bottom(5))

    # todo needs to blow out higher if for etoh
    def magbead_mixing(volume, sc):
        set_speed_profile(p300, 400, 400)
        for _ in range(wash_buffer_reps):
            p300.aspirate(volume * (8 / 10), lb_plt[sc].bottom(0.5))
            p300.dispense(volume * (8 / 10),
                          lb_plt[sc].bottom().move(types.Point(x=-1.75 * int(side[sc]), y=1.5, z=10)))
            p300.aspirate(volume * (8 / 10), lb_plt[sc].bottom(0.5))
            p300.dispense(volume * (8 / 10), lb_plt[sc].bottom().move(types.Point(x=-1.75 * int(side[sc]), y=0, z=10)))
            p300.aspirate(volume * (8 / 10), lb_plt[sc].bottom(0.5))
            p300.dispense(volume * (8 / 10),
                          lb_plt[sc].bottom().move(types.Point(x=-1.75 * int(side[sc]), y=-1.5, z=10)))
        p300.flow_rate.dispense = 50
        p300.blow_out(lb_plt[sc].bottom(dispense_depth))
        exit_well(p300, lb_plt[sc])

    def remove_extraction_buffer(sc, volume):
        p300.flow_rate.aspirate = 25
        p300.aspirate(volume * (8 / 10), lb_plt[sc].bottom().move(types.Point(x=(1 * int(side[sc])), y=0, z=2)))
        protocol.delay(seconds=2)
        p300.aspirate((200 - (volume * (8 / 10))),
                      lb_plt[sc].bottom().move(types.Point(x=(1 * int(side[sc])), y=0, z=0)))
        protocol.delay(seconds=1)

    ####################################################################################################

    # todo: Make these dicts column/sample centric, will require recoding of most of protocol

    # todo: fix alert sound to be 4 beats long and not 5 beats long
    # todo: check status of hardware and configure hardware accordingly 


    protocol.set_rail_lights(True)
    magnetic_module.disengage
    #
    # protocol.pause()
    # play_alert_sound('midpoint.mp3')
    #
    # # protocol.delay(minutes=prok_incubation_time_in_minutes)
    #
    # # mix beads into viral rna buffer
    # p300.pick_up_tip(p300_box1['A1'])
    # set_speed_profile(p300, 300, 300)
    # for _ in range(magbead_buffer_mix_reps):
    #     p300.aspirate(120, nna_lysis_buffer_beads.bottom(1))
    #     p300.dispense(p300.current_volume, nna_lysis_buffer_beads.bottom(10))
    # p300.aspirate(120, nna_lysis_buffer_beads.bottom(1))
    # set_speed_profile(p300, 400, 50)
    # p300.dispense(120, nna_lysis_buffer_beads.bottom(10))
    # p300.blow_out(nna_lysis_buffer_beads.bottom(10))
    # p300.return_tip()
    #
    # # add 2x starting volume of viral rna buffer with beads to each sample
    # p300.pick_up_tip(p300_box1['A1'])
    # aspirate_reagent(p300, (starting_sample_volume * 2), nna_lysis_buffer_beads)
    # p300.dispense(p300.current_volume, lb_plt['A7'].bottom(dispense_depth))
    # exit_well(p300, lb_plt['A7'])
    # p300.return_tip()
    #
    # # fully mix sample with viral rna buffer with beads
    # p300.pick_up_tip(p300_box1['A1'])
    # set_speed_profile(p300, 400, 400)
    # p300.mix(magbead_buffer_mix_reps, (starting_sample_volume * 2), lb_plt['A7'].bottom())
    # exit_well(p300, lb_plt['A7'])
    # p300.return_tip()

    magnetic_module_engage(magbead_binding_time_in_minutes, 6.5)

    # remove buffer from beads
    p300.pick_up_tip(p300_box1['A1'])
    remove_extraction_buffer('A7', 100)
    exit_well(p300, lb_plt['A7'])
    trash_tip(p300)

    magnetic_module.disengage()

    # magbead washes
    p300.pick_up_tip(p300_box1['A2'])
    aspirate_reagent(p300, 100, magbead_nna_wash_1)
    p300.dispense(100, lb_plt['A7'].bottom(dispense_depth))
    exit_well(p300, lb_plt['A7'])
    p300.return_tip()

    # wash beads with magbead buffer
    p300.pick_up_tip(p300_box1['A2'])
    magbead_mixing(100, 'A7')
    exit_well(p300, lb_plt['A7'])
    p300.return_tip()

    # bind magbeads
    magnetic_module_engage(magbead_binding_time_in_minutes, 6.5)

    # remove magbead wash buffer
    p300.pick_up_tip(p300_box1['A2'])
    remove_extraction_buffer('A7', 100)
    exit_well(p300, lb_plt['A7'])
    trash_tip(p300)

    magnetic_module.disengage()

    # magbead washes
    p300.pick_up_tip(p300_box1['A3'])
    aspirate_reagent(p300, 100, magbead_nna_wash_2)
    p300.dispense(100, lb_plt['A7'].bottom(dispense_depth))
    exit_well(p300, lb_plt['A7'])
    p300.return_tip()

    # wash beads with magbead buffer
    p300.pick_up_tip(p300_box1['A3'])
    magbead_mixing(100, 'A7')
    exit_well(p300, lb_plt['A7'])
    p300.return_tip()

    # bind magbeads
    magnetic_module_engage(magbead_binding_time_in_minutes, 6.5)

    # remove magbead wash buffer
    p300.pick_up_tip(p300_box1['A3'])
    remove_extraction_buffer('A7', 100)
    exit_well(p300, lb_plt['A7'])
    trash_tip(p300)

    # unbind magbeads
    magnetic_module.disengage()

    # wash beads with ethanol
    p300.pick_up_tip(p300_box1['A4'])
    aspirate_reagent(p300, 200, ethanol_1)
    extraction_plate_well_wash('A7')
    exit_well(p300, lb_plt['A7'])
    p300.return_tip()

    # mix beads into etoh wash
    p300.pick_up_tip(p300_box1['A4'])
    magbead_mixing(200, 'A7')
    exit_well(p300, lb_plt['A7'])
    p300.return_tip()

    # seperate beads form wash
    magnetic_module_engage(magbead_binding_time_in_minutes, 6.5)

    # remove wash from beads
    p300.pick_up_tip(p300_box1['A4'])
    remove_extraction_buffer('A7', 200)
    exit_well(p300, lb_plt['A7'])
    trash_tip(p300)

    # unbind magbeads
    magnetic_module.disengage()

    # wash beads with ethanol
    p300.pick_up_tip(p300_box1['A5'])
    aspirate_reagent(p300, 200, ethanol_1)
    extraction_plate_well_wash('A7')
    exit_well(p300, lb_plt['A7'])
    p300.return_tip()

    # mix beads into etoh wash

    p300.pick_up_tip(p300_box1['A5'])
    magbead_mixing(200, 'A7')
    exit_well(p300, lb_plt['A7'])
    p300.return_tip()

    # seperate beads form wash
    magnetic_module_engage(magbead_binding_time_in_minutes, 6.5)

    # remove wash from beads
    p300.pick_up_tip(p300_box1['A5'])
    remove_extraction_buffer('A7', 200)
    exit_well(p300, lb_plt['A7'])
    trash_tip(p300)

    # allow residual ethanol to gather at bottom
    protocol.delay(minutes=1)

    # remove residual ethanol 
    p20.pick_up_tip(p20_box1['A1'])
    set_speed_profile(p20, 5, 5)
    p20.aspirate(20, lb_plt['A7'].bottom().move(types.Point(x=-2)))
    p20.move_to(lb_plt['A7'].bottom(0.5).move(types.Point(x=-2)))
    protocol.delay(seconds=1)
    trash_tip(p20)

    # allow beads to dry
    magnetic_module.disengage()
    protocol.delay(minutes=ethanol_dry_time_in_minutes)

    # add eluent
    p20.pick_up_tip(p20_box1['A2'])
    aspirate_reagent(p20, magbead_elution_volume, nf_water)
    set_speed_profile(p20, 30, 30)
    p20.move_to(lb_plt['A7'].bottom(3))
    p20.dispense(magbead_elution_volume, lb_plt['A7'].bottom(3).move(types.Point(x=2)))
    p20.blow_out(lb_plt['A7'].bottom(3).move(types.Point(x=2)))
    p20.move_to(lb_plt['A7'].bottom(1))
    p20.drop_tip()

    protocol.pause() #TEST

    # elute
    p300.pick_up_tip(p300_box1['A6'])
    set_speed_profile(p300, 200, 200)
    p300.mix(10, 15, lb_plt['A7'].bottom())
    exit_well(p300, lb_plt['A7'])
    trash_tip(p300)

    magnetic_module_engage(extraction_elution_bind_time_in_minutes, 7)
