from opentrons import types
import pkg_resources
import json
import subprocess

metadata = {
    'protocolName': 'POLAR',
    'author': 'Per Adastra <adastra.aspera.per@gmail.com>',
    'description': 'Automation of POLAR on OT-2',
    'apiLevel': '2.9'
}

trash_start_int = 0
magbead_elution_volume = 13
prok_control_mix_reps = 10
prok_incubation_time_in_minutes = 15
magbead_binding_time_in_minutes = 5
magbead_buffer_mix_reps = 30
mix_prok_into_sample_reps = 5
wash_buffer_reps = 5
dispense_depth = 5
extraction_elution_bind_time_in_minutes = 5
ethanol_dry_time_in_minutes = 5
spri_bind_time = 5
starting_sample_volume = 50
side = {'A1': -1, 'A2': 1, 'A3': -1, 'A4': 1, 'A5': -1, 'A6': 1, 'A7': -1, 'A8': 1, 'A9': -1, 'A10': 1, 'A11': -1,
        'A12': 1}

def run(protocol):

    def play_alert_sound(sound):
        AUDIO_FILE_PATH = pkg_resources.resource_filename('aidenbots', 'sounds/' + sound)
        # subprocess.run(['mpg123', AUDIO_FILE_PATH], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(AUDIO_FILE_PATH)

    def import_custom_labware(custom_labware_file_name):
        labware_file = pkg_resources.resource_filename('aidenbots', 'labware/' + custom_labware_file_name + '.json')
        with open(labware_file) as labware_def:
            data = json.load(labware_def)
        return data

    # import custom labware
    eppendorf_96_well_lobind_plate_500ul = import_custom_labware("eppendorf_96_well_lobind_plate_500ul")

    # tips
    p300_box1 = protocol.load_labware('opentrons_96_filtertiprack_200ul', '2')
    p300_box2 = protocol.load_labware('opentrons_96_filtertiprack_200ul', '5')
    p300_box3 = protocol.load_labware('opentrons_96_filtertiprack_200ul', '8')
    p300_box4 = protocol.load_labware('opentrons_96_filtertiprack_200ul', '11')
    p20_box1 = protocol.load_labware('opentrons_96_filtertiprack_20ul', '6')
    p20_box2 = protocol.load_labware('opentrons_96_filtertiprack_20ul', '9')

    # pipette hardware
    p300 = protocol.load_instrument('p300_multi_gen2', 'right')
    p20 = protocol.load_instrument('p20_multi_gen2', 'left')

    # modules
    magnetic_module = protocol.load_module('magnetic module gen2', '4')
    temperature_module = protocol.load_module('temperature module gen2', '1')
    thermocycler_module = protocol.load_module('thermocycler')

    # plates & reservoir
    rt_wells = protocol.load_labware('nest_12_reservoir_15ml', '3')
    tc_plt = thermocycler_module.load_labware('biorad_96_wellplate_200ul_pcr')
    cold_reagents = temperature_module.load_labware('biorad_96_wellplate_200ul_pcr')
    lb_plt = magnetic_module.load_labware_from_definition(eppendorf_96_well_lobind_plate_500ul) #TEMP

    # trash Box
    trash_bin = protocol.fixed_trash['A1']

    # rt reagents
    nna_lysis_buffer_beads = rt_wells['A1']
    magbead_nna_wash_1 = rt_wells['A2']
    magbead_nna_wash_2 = rt_wells['A3']
    ethanol_1 = rt_wells['A4']
    ethanol_2 = rt_wells['A5']
    nf_water = rt_wells['A6']
    mineral_oil = rt_wells['A7']
    sparq_beads = rt_wells['A8']
    ethanol_160_proof = rt_wells['A9']
    stop_buffer = rt_wells['A10']
    twb = rt_wells['A11']
    wash_well = rt_wells['A12']

    # cold reagents
    prok = cold_reagents['A1']
    na_shield = cold_reagents['A2']
    warmstart_rt = cold_reagents['A3']
    luna_pcr_mm = cold_reagents['A4']
    eblt_beads = cold_reagents['A5']
    hackflex_buffer = cold_reagents['A6']

    def mag_module_engage(time_in_minutes=0.0, heightin_mm=0.0):
        mag_mod.engage(heightin_mm)
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
        global trash_start_int
        if trash_start_int == 18:
            trash_start_int = 0
        else:
            trash_start_int += 1
        if instrument == p300:
            set_speed_profile(p300, 200, 200)
            if instrument.current_volume > 20:
                instrument.dispense(instrument.current_volume,p20_box2['A12'].top().move(types.Point(x=30, y=0, z=-20)))
                instrument.move_to(p20_box2['A12'].top().move(types.Point(x=30, y=0, z=20)))
                instrument.move_to(trash_bin.top().move(types.Point(x=70, y=-10, z=35)))
            else:
                p300.move_to(trash_bin.top().move(types.Point(x=-20, y=-10, z=40)))
            instrument.drop_tip(trash_bin.top().move(types.Point(x=(-20 + (5 * trash_start_int)), y=-10, z=20)))
            p300.move_to(trash_bin.top().move(types.Point(x=-20, y=-10, z=40)))
        else:
            instrument.drop_tip()

    def remove_bead_wash_buffer(volume, sc):
        p300.flow_rate.aspirate = 5
        for _ in range(3):
            p300.aspirate((volume / 3), lb_plt[sc].bottom(0.5).move(types.Point(x=2 * int(side[sc]))))
            protocol.delay(seconds=3)

    def elute_in_q5u(sc, volume=20):
        set_speed_profile(p300, 200, 50)
        p300.move_to(lb_plt[sc].bottom().move(types.Point(z=5)))
        p300.dispense(20, lb_plt[sc].bottom().move(types.Point(x=-2 * int(side[sc]), y=0, z=5)))
        p300.blow_out(lb_plt[sc].bottom().move(types.Point(x=-2 * int(side[sc]), y=0, z=5)))
        for _ in range(5):
            p300.aspirate(volume, lb_plt[sc].bottom(0.5))
            p300.dispense(volume, lb_plt[sc].bottom().move(types.Point(x=-2 * int(side[sc]), y=1.5, z=5)))
            p300.aspirate(volume, lb_plt[sc].bottom(0.5))
            p300.dispense(volume,lb_plt[sc].bottom().move(types.Point(x=-2 * int(side[sc]), y=0, z=5)))
            p300.aspirate(volume, lb_plt[sc].bottom(0.5))
            p300.dispense(volume, lb_plt[sc].bottom().move(types.Point(x=-2 * int(side[sc]), y=-1.5, z=5)))
        set_speed_profile(p300, 200, 200)
        p300.mix(10, volume * (3 / 4), lb_plt[sc].bottom(1))
        p300.blow_out(lb_plt[sc].bottom(5))

    def extraction_plate_well_wash(sc):
        p300.move_to(lb_plt[sc].top(-3))
        p300.dispense(50, lb_plt[sc].top().move(types.Point(x=-3.2, y=0, z=-3)))
        p300.dispense(50, lb_plt[sc].top().move(types.Point(x=+3.2, y=0, z=-3)))
        p300.dispense(50, lb_plt[sc].top().move(types.Point(x=0, y=+3.2, z=-3)))
        p300.dispense(50, lb_plt[sc].top().move(types.Point(x=0, y=-3.2, z=-3)))
        p300.move_to(lb_plt[sc].top(-3))

    def elute_na_from_beads(sc, volume=20):
        set_speed_profile(p300, 200, 50)
        p300.move_to(lb_plt[sc].bottom().move(types.Point(z=5)))
        p300.dispense(20, lb_plt[sc].bottom().move(types.Point(x=-2 * int(side[sc]), y=0, z=5)))
        p300.blow_out(lb_plt[sc].bottom().move(types.Point(x=-2 * int(side[sc]), y=0, z=5)))
        for _ in range(5):
            p300.aspirate(volume, lb_plt[sc].bottom(0.5))
            p300.dispense(volume, lb_plt[sc].bottom().move(types.Point(x=-2 * int(side[sc]), y=1.5, z=5)))
            p300.aspirate(volume, lb_plt[sc].bottom())
            p300.dispense(volume,lb_plt[sc].bottom().move(types.Point(x=-2 * int(side[sc]), y=0, z=5)))
            p300.aspirate(volume, lb_plt[sc].bottom())
            p300.dispense(volume, lb_plt[sc].bottom().move(types.Point(x=-2 * int(side[sc]), y=-1.5, z=5)))
        set_speed_profile(p300, 200, 200)
        p300.mix(10, volume * (3 / 4), lb_plt[sc].bottom())
        p300.blow_out(lb_plt[sc].bottom(5))

    #todo needs to blow out higher if for etoh
    def magbead_mixing(volume, sc):
        set_speed_profile(p300, 400, 400)
        for _ in range(wash_buffer_reps):
            p300.aspirate(volume * (8 / 10), lb_plt[sc].bottom(0.5))
            p300.dispense(volume * (8 / 10), lb_plt[sc].bottom().move(types.Point(x=-1.75 * int(side[sc]), y=1.5, z=10)))
            p300.aspirate(volume * (8 / 10), lb_plt[sc].bottom(0.5))
            p300.dispense(volume * (8 / 10), lb_plt[sc].bottom().move(types.Point(x=-1.75 * int(side[sc]), y=0, z=10)))
            p300.aspirate(volume * (8 / 10), lb_plt[sc].bottom(0.5))
            p300.dispense(volume * (8 / 10), lb_plt[sc].bottom().move(types.Point(x=-1.75 * int(side[sc]), y=-1.5, z=10)))
        p300.flow_rate.dispense = 50
        p300.blow_out(lb_plt[sc].bottom(dispense_depth))
        exit_well(p300, lb_plt[sc])

    def remove_extraction_buffer(sc, volume):
        p300.flow_rate.aspirate = 25
        p300.aspirate(volume * (8 / 10), lb_plt[sc].bottom().move(types.Point(x=(1 * int(side[sc])), y=0, z=2)))
        protocol.delay(seconds=2)
        p300.aspirate((200 - (volume * (8 / 10))), lb_plt[sc].bottom().move(types.Point(x=(1 * int(side[sc])), y=0, z=0)))
        protocol.delay(seconds=1)


    # magbead_nna_wash_1 = {'name': 'magbead_nna_wash_1',
    #                       'reagent': magbead_nna_wash_1,
    #                       'sc': right_column_names,
    #                       'tip': left_column_names}
    #
    # magbead_nna_wash_2 = {'name': 'magbead_nna_wash_2',
    #                       'reagent': magbead_nna_wash_2,
    #                       'sc': right_column_names,
    #                       'tip': right_column_names}
    #
    # ethanol_1_wash = {'name': 'ethanol_1_wash',
    #                   'reagent': ethanol_1,
    #                   'sc': right_column_names,
    #                   'tip': left_column_names}
    #
    # ethanol_2_wash = {'name': 'ethanol_2_wash',
    #                   'reagent': ethanol_2,
    #                   'sc': right_column_names,
    #                   'tip': right_column_names}


    protocol.set_rail_lights(True)
    magnetic_module.disengage()
    protocol.pause()
    play_alert_sound('midpoint.mp3') #todo fix sound file

#     # add 1X nn shield with control to protinase k
#     # larger volume reagents are always mixed into smaller volume reagents
#     p300.pick_up_tip(p300_box1['A7'])
#     p300.aspirate(70, na_shield.bottom(1))
#     set_speed_profile(p300, 50, 50)
#     p300.mix(prok_control_mix_reps, 50, prok.bottom(1))
#     p300.blow_out(prok.bottom(5))
#     exit_well(p300, prok)
#     p300.return_tip()
#
#     # add protinase k, 1x na shield with control to all samples
#     for sc, tip in zip(right_column_names, left_column_names):
#         p20.pick_up_tip(p20_box1[tip])
#         aspirate_reagent(p20, 10, prok)
#         p20.dispense(10, lb_plt[sc].bottom(1))
#         # trash_tip(p20)
#         p20.return_tip() #TESTING
#
#     # fully mix prok, 1x nn shield and control reagents into samples
#     for sc, tip in zip(right_column_names, left_column_names):
#         p300.pick_up_tip(p300_box1[tip])
#         set_speed_profile(p300, 300, 300)
#         p300.mix(mix_prok_into_sample_reps, 50, lb_plt[sc].bottom())
#         exit_well(p300, lb_plt[sc])
#         # trash_tip(p300)
#         p300.return_tip() #TESTING
#
#     protocol.delay(minutes=prok_incubation_time_in_minutes)
#
#     # # mix beads into viral rna buffer
#     p300.pick_up_tip(p300_box1['A7'])
#     set_speed_profile(p300, 300, 300)
#     for _ in range(magbead_buffer_mix_reps):
#         p300.aspirate(120, nna_lysis_buffer_beads.bottom(1))
#         p300.dispense(p300.current_volume, nna_lysis_buffer_beads.bottom(10))
#     p300.aspirate(120, nna_lysis_buffer_beads.bottom(1))
#     set_speed_profile(p300, 400, 50)
#     p300.dispense(120, nna_lysis_buffer_beads.bottom(10))
#     p300.blow_out(nna_lysis_buffer_beads.bottom(10))
#     p300.return_tip()
#
#     # add 2x starting volume of viral rna buffer with beads to each sample
#     for sc, tip in zip(right_column_names, right_column_names):
#         p300.pick_up_tip(p300_box1[tip])
#         aspirate_reagent(p300, ((starting_sample_volume + 10) * 2), nna_lysis_buffer_beads)
#         p300.dispense(((starting_sample_volume + 10) * 2),
#                       lb_plt[sc].bottom(dispense_depth))
#         exit_well(p300, lb_plt[sc])
#         p300.return_tip()
#
#     # fully mix sample with viral rna buffer with beads
#     for sc, tip in zip(right_column_names, right_column_names):
#         p300.pick_up_tip(p300_box1[tip])
#         set_speed_profile(p300, 400, 400)
#         p300.mix(mix_prok_into_sample_reps, 150, lb_plt[sc].bottom())
#         exit_well(p300, lb_plt[sc])
#         p300.return_tip()
#
#     mag_module_engage(magbead_binding_time_in_minutes, 6.5)
#
#     # # remove buffer from beads
#     for sc, tip in zip(right_column_names, right_column_names):
#         p300.pick_up_tip(p300_box1[tip])
#         remove_extraction_buffer(sc, 100)
#         exit_well(p300, lb_plt[sc])
#         # trash_tip(p300)
#         p300.return_tip() #TESTING
#
#     mag_module.disengage()
#
#     # magbead washes
#     for wash in (magbead_nna_wash_1, magbead_nna_wash_2):
#
#         # add magbead wash to samples
#         for sc, tip in zip(wash['sc'], wash['tip']):
#             p300.pick_up_tip(p300_box2[tip])
#             aspirate_reagent(p300, 100, wash['reagent'])
#             p300.dispense(100, lb_plt[sc].bottom(dispense_depth))
#             exit_well(p300, lb_plt[sc])
#             p300.return_tip()
#
#         # wash beads with magbead buffer
#         for sc, tip in zip(wash['sc'], wash['tip']):
#             p300.pick_up_tip(p300_box2[tip])
#             magbead_mixing(100, sc)
#             exit_well(p300, lb_plt[sc])
#             p300.return_tip()
#
#         # bind magbeads
#         mag_module_engage(magbead_binding_time_in_minutes, 6.5)
#
#         # remove magbead wash buffer
#         for sc, tip in zip(wash['sc'], wash['tip']):
#             p300.pick_up_tip(p300_box2[tip])
#             remove_extraction_buffer(sc, 100)
#             exit_well(p300, lb_plt[sc])
#             trash_tip(p300)
#
#         # unbind magbeads
#         mag_mod.disengage()
#
#     # etoh wash #1
#     for wash in (ethanol_1_wash, ethanol_2_wash):
#
#         # add etoh wash
#         for sc, tip in zip(wash['sc'], wash['tip']):
#             p300.pick_up_tip(p300_box3[tip])
#             aspirate_reagent(p300, 200, ethanol_1)
#             extraction_plate_well_wash(sc)
#             exit_well(p300, lb_plt[sc])
#             p300.return_tip()
#
#         # mix beads into etoh wash
#         for sc, tip in zip(wash['sc'], wash['tip']):
#             p300.pick_up_tip(p300_box3[tip])
#             magbead_mixing(200, sc)
#             exit_well(p300, lb_plt[sc])
#             p300.return_tip()
#
#         # seperate beads form wash
#         mag_module_engage(magbead_binding_time_in_minutes, 6.5)
#
#         if wash['name'] == 'ethanol_2_wash':
#             thermo_mod.set_block_temperature(4)
#             thermo_mod.set_lid_temperature(105)
#
#             # mix luna mm w/ primers and hexamers into rt enzyme
#             p300.pick_up_tip(p300_box4['A7'])
#             set_speed_profile(p300, 20, 20)
#             p300.aspirate(100, luna_pcr_mm.bottom())
#             p300.dispense(p300.current_volume, warmstart_rt.bottom(2))
#             set_speed_profile(p300, 50, 50)
#             p300.mix(10, 85, warmstart_rt.bottom(1))
#             exit_well(p300, warmstart_rt)
#             p300.blow_out(warmstart_rt.top())
#             p300.return_tip()
#
#             # add rt-pcr mm to all wells
#             p20.pick_up_tip(p20_box1['A7'])
#             for sc in right_column_names:
#                 p20.aspirate(7, warmstart_rt.top())
#                 aspirate_reagent(p20, 13, warmstart_rt)
#                 p20.dispense(20, tc_plt[sc].bottom(1))
#                 exit_well(p20, tc_plt[sc])
#             p20.return_tip()
#
#             # add oil to all wells
#             p300.pick_up_tip(p300_box4['A7'])
#             aspirate_reagent(p300, 200, mineral_oil)
#             for sc in right_column_names:
#                 side_dispense(p300, 30, tc_plt[sc])
#                 p300.blow_out(mineral_oil.top(-10))
#                 set_speed_profile(p300, 200, 200)
#                 p300.mix(5, 200, wash_well.bottom(1))
#                 p300.blow_out(wash_well.top())
#             p300.return_tip()
#
#         # remove wash from beads
#         for sc, tip in zip(wash['sc'], wash['tip']):
#             p300.pick_up_tip(p300_box3[tip])
#             remove_extraction_buffer(sc, 200)
#             exit_well(p300, lb_plt[sc])
#             trash_tip(p300)
#
#         if wash['name'] == 'ethanol_2_wash':
#             for sc, tip in zip(wash['sc'], wash['tip']):
#                 p20.pick_up_tip(p20_box1[tip])
#                 set_speed_profile(p20, 5, 5)
#                 p20.aspirate(20, lb_plt[sc].bottom().move(
#                     types.Point(x=2 * side[sc])))
#                 p20.move_to(lb_plt[sc].bottom(0.5).move(
#                     types.Point(x=2 * side[sc])))
#                 protocol.delay(seconds=1)
#                 trash_tip(p20)
#
#         mag_mod.disengage()
# #
# #     ### ^ TESTED BOOKMARK ^ ###
# #
# #         # protocol.delay(minutes=ethanol_dry_time_in_minutes)
# #
# #         # Add elution buffer and try to get beads off wall
# #         for sc, tip in zip(right_column_names, left_column_names):
# #             p20.pick_up_tip(p20_box2[tip])
# #             aspirate_reagent(p20, magbead_elution_volume, nf_water)
# #             set_speed_profile(p20, 30, 30)
# #             p20.move_to(lb_plt[sc].bottom(3))
# #             p20.dispense(magbead_elution_volume, lb_plt[sc].bottom(3).move(
# #                             types.Point(x=-2 * int(side[sc]))))
# #             p20.blow_out(lb_plt[sc].bottom(3).move(
# #                             types.Point(x=-2 * int(side[sc]))))
# #             p20.move_to(lb_plt[sc].bottom(1))
# #             p20.return_tip()
# #
# #         # fully elute samples
# #         for sc, tip in zip(right_column_names, left_column_names):
# #             p300.pick_up_tip(p300_box4[tip])
# #             set_speed_profile(p300, 200, 200)
# #             p300.mix(10, 15, lb_plt[sc].bottom())
# #             exit_well(p300, lb_plt[sc])
# #             trash_tip(p300)
# #
# #         mag_module_engage(extraction_elution_bind_time_in_minutes, 7)
# #
# #         # transfer elution to thermocycler plate
# #         for sc, tip in zip(right_column_names, left_column_names):
# #             p20.pick_up_tip(p20_box2[tip])
# #             set_speed_profile(p20, 2.5, 2.5)
# #             p20.aspirate(7, lb_plt[sc].bottom().move(
# #                 types.Point(x=2 * int(side[sc]))))
# #             p20.dispense(p20.current_volume, tc_plt[sc].bottom())
# #             p20.mix(2, 7, tc_plt[sc].bottom())
# #             exit_well(p20, tc_plt[sc])
# #             trash_tip(p20)
# #
# #         # drops magnet to prevent magebads from sticking to lobind plate
# #         mag_mod.disengage()
# #
# #         protocol.home()
# #
# #         # perform amplicon pcr
# #         thermo_mod.close_lid()
# #
# #         thermo_mod.set_block_temperature(55.0, hold_time_minutes=15, block_max_volume=20)
# #         thermo_mod.set_block_temperature(95.0, hold_time_seconds=75, block_max_volume=20)
# #         thermo_mod.execute_profile([{'temperature': 95, 'hold_time_seconds': 15},
# #                                     {'temperature': 63, 'hold_time_minutes': 3}],
# #                                    repetitions=25,
# #                                    block_max_volume=20)
# #         thermo_mod.set_block_temperature(25, block_max_volume=20)
# #
# #         thermo_mod.open_lid()
# #
# #         protocol.home()
# #
# #         # resuspend sparq beads which have pelleted
# #         set_speed_profile(p300, 100, 100)
# #         p300.pick_up_tip(p300_box4['A7'])
# #         p300.mix(10, 100, sparq_beads.bottom(1))
# #         exit_well(p300, sparq_beads)
# #         trash_tip(p300)
# #
# #         # add sparq beads to all the samples
# #         for sc, tip in zip(right_column_names, right_column_names):
# #             p20.pick_up_tip(p20_box2[tip])
# #             aspirate_reagent(p20, 15, sparq_beads)
# #             side_dispense(p20, p20.current_volume, tc_plt[sc])
# #             trash_tip(p20)
# #
# #         thermo_mod.close_lid()
# #
# #     #     # clean out magbeads from well for use later
# #     #     for sc, tip in zip(right_column_names, right_column_names):
# #     #         p300.pick_up_tip(p300_box4[tip])
# #     #         aspirate_reagent(p300, 100, nf_water)
# #     #         set_speed_profile(p300, 200, 200)
# #     #         p300.dispense(100, lb_plt[sc].bottom())
# #     #         p300.mix(5, 100, lb_plt[sc].bottom())
# #     #         set_speed_profile(p300, 50, 50)
# #     #         p300.aspirate(200, lb_plt[sc].bottom())
# #     #         trash_tip(p300)
# #     #
# #     #     # move head out of the way
# #     #     p20.move_to(cold_reagents['A1'].top(20))
# #     #
# #     #     # visual alert
# #     #     flash()
# #     #     # audio alert
# #     #     play_alert_sound('midpoint')
# #     #     protocol.pause()
# #     #
# #     #     thermo_mod.open_lid()
# #     #
# #     #     for sc, tip in zip(right_column_names, left_column_names):
# #     #         p300.pick_up_tip(p300_box1[tip])
# #     #         set_speed_profile(p300, 200, 200)
# #     #         p300.mix(10, 50, tc_plt[sc].bottom(1))
# #     #         set_speed_profile(p300, 50, 50)
# #     #         for _ in range(2):
# #     #             p300.aspirate(40, tc_plt[sc].bottom())
# #     #             protocol.delay(seconds=1)
# #     #         p300.aspirate(20, tc_plt[sc].bottom(-0.5))
# #     #         exit_well(p300, tc_plt[sc])
# #     #         p300.dispense(p300.current_volume, lb_plt[sc].bottom(1))
# #     #         exit_well(p300, lb_plt[sc])
# #     #         p300.return_tip()
# #     #
# #     #     mag_module_engage(spri_bind_time, 7)
# #     #
# #     #     for sc, tip in zip(right_column_names, left_column_names):
# #     #         p300.pick_up_tip(p300_box1[tip])
# #     #         remove_bead_wash_buffer(60, sc)
# #     #         exit_well(p300, lb_plt[sc])
# #     #         p300.return_tip()
# #     #
# #     #     for sc, tip in zip(right_column_names, right_column_names):
# #     #         p300.pick_up_tip(p300_box1[tip])
# #     #         aspirate_reagent(p300, 100, ethanol_160_proof)
# #     #         p300.dispense(p300.current_volume, lb_plt[sc].bottom(dispense_depth))
# #     #         exit_well(p300, lb_plt[sc])
# #     #         p300.return_tip()
# #     #
# #     #     for sc, tip in zip(right_column_names, right_column_names):
# #     #         p300.pick_up_tip(p300_box1[tip])
# #     #         remove_bead_wash_buffer(100, sc)
# #     #         exit_well(p300, lb_plt[sc])
# #     #         trash_tip(p300)
# #     #
# #     #     mag_module_engage(0, 0)
# #     #
# #     #     protocol.delay(minutes=2)
# #     #
# #     #     p300.pick_up_tip(p300_box2['A1'])
# #     #     set_speed_profile(p300, 50, 50)
# #     #     aspirate_reagent(p300, 50, hackflex_buffer)
# #     #     p300.dispense(50, eblt_beads.bottom(1))
# #     #     set_speed_profile(p300, 200, 200)
# #     #     p300.mix(20, 40, eblt_beads.bottom(1))
# #     #     exit_well(p300, eblt_beads)
# #     #     p300.return_tip()
# #     #
# #     #     for sc, tip in zip(right_column_names, left_column_names):
# #     #         p300.pick_up_tip(p300_box2[tip])
# #     #         aspirate_reagent(p300, 25, nf_water)
# #     #         elute_na_from_beads(sc, volume=25)
# #     #         exit_well(p300, lb_plt[sc])
# #     #         p300.return_tip()
# #     #
# #     #     mag_module_engage(spri_bind_time, 6.5)
# #     #
# #     #     thermo_mod.set_block_temperature(10)
# #     #
# #     #     for sc, tip, thermocycler_well in zip(right_column_names, left_column_names, right_column_names):
# #     #         p20.pick_up_tip(p20_box1[tip])
# #     #         aspirate_reagent(p20, 6, eblt_beads)
# #     #         p20.dispense(6, tc_plt[thermocycler_well].bottom())
# #     #         p20.aspirate(20, lb_plt[sc].bottom().move(types.Point(x=1, y=0, z=0)))
# #     #         exit_well(p20, lb_plt[sc])
# #     #         set_speed_profile(p20, 30, 30)
# #     #         p20.dispense(20, tc_plt[thermocycler_well].bottom())
# #     #         p20.mix(10, 15, tc_plt[thermocycler_well].bottom(1))
# #     #         exit_well(p20, tc_plt[thermocycler_well])
# #     #         p20.return_tip()
# #     #
# #     #     protocol.home()
# #     #
# #     #     flash()
# #     #     thermo_mod.close_lid()
# #     #     thermo_mod.set_block_temperature(55.0,
# #     #                                      hold_time_minutes=5,
# #     #                                      block_max_volume=26)
# #     #     thermo_mod.set_block_temperature(25.0,
# #     #                                      block_max_volume=26)
# #     #     thermo_mod.open_lid()
# #     #
# #     #     for sc, tip in zip(right_column_names,
# #     #                                   right_column_names):
# #     #         p20.pick_up_tip(p20_box1[tip])
# #     #         aspirate_reagent(p20, 5, stop_buffer)
# #     #         p20.dispense(p20.current_volume,
# #     #                      tc_plt[sc].bottom())
# #     #         exit_well(p20,
# #     #                   tc_plt[sc])
# #     #         p20.return_tip()
# #     #
# #     #     for sc, sc_end, tip in zip(right_column_names,
# #     #                                                      left_column_names,
# #     #                                                      left_column_names):
# #     #         p300.pick_up_tip(p300_box2[tip])
# #     #         for i in range(2):
# #     #             p300.aspirate(40, tc_plt[sc].bottom())
# #     #             protocol.delay(seconds=1)
# #     #         p300.aspirate(20, tc_plt[sc].bottom(-0.5))
# #     #         p300.dispense(p300.current_volume, lb_plt[sc_end].bottom(1))
# #     #         set_speed_profile(p300, 50, 50)
# #     #         p300.mix(10, 50, lb_plt[sc_end].bottom(1))
# #     #         p300.flow_rate.blow_out = 50
# #     #         p300.blow_out(lb_plt[sc_end].bottom(5))
# #     #         exit_well(p300, lb_plt[sc_end])
# #     #         p300.return_tip()
# #     #
# #     #     mag_module_engage(10, 6.5)
# #     #
# #     #     for sc, tip in zip(left_column_names, left_column_names):
# #     #         p300.pick_up_tip(p300_box2[tip])
# #     #         remove_bead_wash_buffer(30, sc)
# #     #         exit_well(p300, lb_plt[sc])
# #     #         trash_tip(p300)
# #     #
# #     #     for sc, tip in zip(left_column_names, right_column_names):
# #     #         p300.pick_up_tip(p300_box2[tip])
# #     #         aspirate_reagent(p300, 50, twb)
# #     #         p300.dispense(p300.current_volume, lb_plt[sc].bottom(dispense_depth))
# #     #         exit_well(p300, lb_plt[sc])
# #     #         trash_tip(p300)
# #     #
# #     #     for sc, tip in zip(left_column_names, right_column_names):
# #     #         p300.pick_up_tip(p300_box2[tip])
# #     #         remove_bead_wash_buffer(50, sc)
# #     #         exit_well(p300, lb_plt[sc])
# #     #         trash_tip(p300)
# #     #
# #     #     mag_module_engage(0, 0)
# #     #
# #     #     for sc, tip, index, sc_end in zip(left_column_names,
# #     #                                                             left_column_names,
# #     #                                                             right_column_names,
# #     #                                                             right_column_names):
# #     #         p300.pick_up_tip(p300_box3[tip])
# #     #         aspirate_reagent(p300, 30, cold_reagents[index])
# #     #         elute_in_q5u(sc, side[sc])
# #     #         set_speed_profile(p300, 15, 15)
# #     #         for i in range(2):
# #     #             p300.aspirate(20, lb_plt[sc].bottom())
# #     #             protocol.delay(seconds=2)
# #     #         exit_well(p300, lb_plt[sc])
# #     #         side_dispense(p300, p300.current_volume, tc_plt[sc_end])
# #     #         exit_well(p300, tc_plt[sc_end])
# #     #         trash_tip(p300)
# #     #
# #     #     protocol.home()
# #     #     thermo_mod.set_lid_temperature(105)
# #     #     thermo_mod.close_lid()
# #     #     thermo_mod.set_block_temperature(98.0, hold_time_seconds=30, block_max_volume=20)
# #     #     thermo_mod.execute_profile([{'temperature': 98, 'hold_time_seconds': 15},
# #     #                                 {'temperature': 63, 'hold_time_seconds': 30},
# #     #                                 {'temperature': 65, 'hold_time_seconds': 15}],
# #     #                                repetitions=6,
# #     #                                block_max_volume=20)
# #     #     thermo_mod.set_block_temperature(25, hold_time_minutes=1, block_max_volume=20)
# #     #     thermo_mod.open_lid()
# #     #     protocol.home()
# #     #
# #     #     p300.pick_up_tip(p300_box3['A7'])
# #     #     aspirate_reagent(p300, 100, nf_water)
# #     #     p300.dispense(100, lb_plt['A12'].bottom())
# #     #     set_speed_profile(p300, 200, 200)
# #     #     p300.mix(10, 100, lb_plt['A12'].bottom())
# #     #     set_speed_profile(p300, 10, 200)
# #     #     p300.aspirate(200, lb_plt['A12'].bottom())
# #     #     trash_tip(p300)
# #     #
# #     #     p300.pick_up_tip(p300_box3['A8'])
# #     #     aspirate_reagent(p300, 30, sparq_beads)
# #     #     p300.dispense(p300.current_volume, lb_plt['A12'].bottom())
# #     #     set_speed_profile(p300, 50, 50)
# #     #     for column in right_column_names:
# #     #         p300.aspirate(20, tc_plt[column].bottom())
# #     #     p300.dispense(p300.current_volume, tc_plt['A12'].bottom())
# #     #     p300.mix(10, 50, tc_plt['A12'].bottom())
# #     #     p300.aspirate(30, tc_plt['A12'].bottom())
# #     #     p300.dispense(p300.current_volume, lb_plt['A12'].bottom(1))
# #     #     p300.mix(10, 30, lb_plt['A12'].bottom())
# #     #
# #     #     mag_module_engage(spri_bind_time, 7)
# #     #
# #     #     remove_bead_wash_buffer(50, 'A12')
# #     #     trash_tip(p300)
# #     #
# #     #     p300.pick_up_tip(p300_box3['A9'])
# #     #     aspirate_reagent(p300, 100, ethanol_160_proof)
# #     #     p300.dispense(p300.current_volume, lb_plt['A12'].bottom(1))
# #     #     protocol.delay(minutes=1)
# #     #     set_speed_profile(p300, 100, 100)
# #     #     p300.aspirate(200, tc_plt['A12'].bottom())
# #     #     trash_tip(p300)
# #     #
# #     #     p300.pick_up_tip(p300_box3['A10'])
# #     #     p300.aspirate(200, tc_plt['A12'].bottom())
# #     #     trash_tip(p300)
# #     #
# #     #     mag_module_engage(0, 0)
# #     #
# #     #     protocol.delay(minutes=3)
# #     #
# #     #     p300.pick_up_tip(p300_box3['A11'])
# #     #     aspirate_reagent(p300, 20, nf_water)
# #     #     p300.dispense(p300.current_volume, lb_plt['A12'].bottom(1))
# #     #     protocol.delay(minutes=1)
# #     #     set_speed_profile(p300, 100, 100)
# #     #     p300.mix(10, 20, lb_plt['A12'].bottom(1))
# #     #     trash_tip(p300)
# #     #
# #     #     protocol.delay(minutes=3)
# #     #
# #     #     p300.pick_up_tip(p300_box3['G12'])
# #     #     p300.mix(5, 20, lb_plt['A12'].bottom(1))
# #     #     p300.aspirate(20, lb_plt['A12'].bottom())
# #     #     p300.dispense(p300.current_volume, lb_plt['A12'].bottom(1))
# #     #
# #     #     mag_module_engage(spri_bind_time, 7)
# #     #
# #     #     for well in 'B12' 'C12' 'D12' 'E12' 'F12' 'G12' 'H12':
# #     #         set_speed_profile(p300, 40, 40)
# #     #         p300.aspirate(40, lb_plt[well].bottom())
# #     #         p300.dispense(p300.current_volume, lb_plt['A12'].bottom(1))
# #     #
# #     #     p300.mix(5, 60, lb_plt['A12'].bottom(1))
# #     #     trash_tip(p300)
