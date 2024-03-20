import csv

import javalang

from metrics_collection.ast_metrics import NotClassError, attrs_, sattrs_, ctors_, methods_, smethods_, ncss_, impls_, \
    extnds_, gnrcs_, final_, annts_, varcomp_, mhf_, smhf_, ahf_, sahf_, nomp_, nosmp_, mxnomp_, mxnosmp_, nom_, \
    nop_, nulls_, doer_


class CodeMetrics:
    def __init__(self, trees, repozitory_name):
        self.min_nooa = 0
        self.max_nooa = 1000000
        self.total_nooa = 0
        self.nooa = 0

        self.min_nosa = 0
        self.max_nosa = 1000000
        self.total_nosa = 0
        self.nosa = 0
        self.min_nocc = 0
        self.max_nocc = 1000000
        self.total_nocc = 0
        self.nocc = 0
        self.min_noom = 0
        self.max_noom = 1000000
        self.total_noom = 0
        self.noom = 0
        self.min_nocm = 0
        self.max_nocm = 1000000
        self.total_nocm = 0
        self.nocm = 0
        self.min_ncss = 0
        self.max_ncss = 1000000
        self.total_ncss = 0
        self.ncss = 0
        self.min_noii = 0
        self.max_noii = 1000000
        self.total_noii = 0
        self.noii = 0
        self.min_napc = 0
        self.max_napc = 1000000
        self.total_napc = 0
        self.napc = 0
        self.min_notp = 0
        self.max_notp = 1000000
        self.total_notp = 0
        self.notp = 0
        self.min_final = 0
        self.max_final = 1000000
        self.total_final = 0
        self.final = 0
        self.min_noca = 0
        self.max_noca = 1000000
        self.total_noca = 0
        self.noca = 0
        self.min_varcomp = 0
        self.max_varcomp = 1000000
        self.total_varcomp = 0
        self.varcomp = 0
        self.min_mhf = 0
        self.max_mhf = 1000000
        self.total_mhf = 0
        self.mhf = 0
        self.min_smhf = 0
        self.max_smhf = 1000000
        self.total_smhf = 0
        self.smhf = 0
        self.min_ahf = 0
        self.max_ahf = 1000000
        self.total_ahf = 0
        self.ahf = 0
        self.min_sahf = 0
        self.max_sahf = 1000000
        self.total_sahf = 0
        self.sahf = 0
        self.min_nomp = 0
        self.max_nomp = 1000000
        self.total_nomp = 0
        self.nomp = 0
        self.min_nosmp = 0
        self.max_nosmp = 1000000
        self.total_nosmp = 0
        self.nosmp = 0
        self.min_mxnomp = 0
        self.max_mxnomp = 1000000
        self.total_mxnomp = 0
        self.mxnomp = 0
        self.min_mxnosmp = 0
        self.max_mxnosmp = 1000000
        self.total_mxnosmp = 0
        self.mxnosmp = 0
        self.min_nom = 0
        self.max_nom = 1000000
        self.total_nom = 0
        self.nom = 0
        self.min_nop = 0
        self.max_nop = 1000000
        self.total_nop = 0
        self.nop = 0
        self.min_nulls = 0
        self.max_nulls = 1000000
        self.total_nulls = 0
        self.nulls = 0
        self.min_doer = 0
        self.max_doer = 1000000
        self.total_doer = 0
        self.doer = 0
        self.trees = trees
        self.repozitory_name = repozitory_name
        self.count_metrics()
        self.aver_nooa = self.nooa / self.total_nooa if self.total_nooa != 0 else 0
        self.aver_nosa = self.nosa / self.total_nosa if self.total_nosa != 0 else 0
        self.aver_nocc = self.nocc / self.total_nocc if self.total_nocc != 0 else 0
        self.aver_noom = self.noom / self.total_noom if self.total_noom != 0 else 0
        self.aver_nocm = self.nocm / self.total_nocm if self.total_nocm != 0 else 0
        self.aver_ncss = self.ncss / self.total_ncss if self.total_ncss != 0 else 0
        self.aver_noii = self.noii / self.total_noii if self.total_noii != 0 else 0
        self.aver_napc = self.napc / self.total_napc if self.total_napc != 0 else 0
        self.aver_notp = self.notp / self.total_notp if self.total_notp != 0 else 0
        self.aver_final = self.final / self.total_final if self.total_final != 0 else 0
        self.aver_noca = self.noca / self.total_noca if self.total_noca != 0 else 0
        self.aver_varcomp = self.varcomp / self.total_varcomp if self.total_varcomp != 0 else 0
        self.aver_mhf = self.mhf / self.total_mhf if self.total_mhf != 0 else 0
        self.aver_smhf = self.smhf / self.total_smhf if self.total_smhf != 0 else 0
        self.aver_ahf = self.ahf / self.total_ahf if self.total_ahf != 0 else 0
        self.aver_sahf = self.sahf / self.total_sahf if self.total_sahf != 0 else 0
        self.aver_nomp = self.nomp / self.total_nomp if self.total_nomp != 0 else 0
        self.aver_nosmp = self.nosmp / self.total_nosmp if self.total_nosmp != 0 else 0
        self.aver_mxnomp = self.mxnomp / self.total_mxnomp if self.total_mxnomp != 0 else 0
        self.aver_mxnosmp = self.mxnosmp / self.total_mxnosmp if self.total_mxnosmp != 0 else 0
        self.aver_nom = self.nom / self.total_nom if self.total_nom != 0 else 0
        self.aver_nop = self.nop / self.total_nop if self.total_nop != 0 else 0
        self.aver_nulls = self.nulls / self.total_nulls if self.total_nulls != 0 else 0
        self.aver_doer = self.doer / self.total_doer if self.total_doer != 0 else 0
        self.save_metrics()

    def count_metrics(self):
        for raw in self.trees:
            tree = raw.filter(javalang.tree.ClassDeclaration)
            if not (tree_class := list((value for value in tree))):
                raise NotClassError('This is not a class')
            nooa = attrs_(tree_class)
            print(f'repository = {self.repozitory_name}\tnooa = {nooa}')
            self.min_nooa = min(nooa, self.min_nooa)
            self.max_nooa = max(nooa, self.max_nooa)
            self.total_nooa += 1
            self.nooa += nooa

            nosa = sattrs_(tree_class)
            print(f'repository = {self.repozitory_name}\tnosa = {nosa}')
            self.min_nosa = min(nosa, self.min_nosa)
            self.max_nosa = max(nosa, self.max_nosa)
            self.total_nosa += 1
            self.nosa += nosa

            nocc = ctors_(tree_class)
            print(f'repository = {self.repozitory_name}\tnocc = {nocc}')
            self.min_nocc = min(nocc, self.min_nocc)
            self.max_nocc = max(nocc, self.max_nocc)
            self.total_nocc += 1
            self.nocc += nocc

            noom = methods_(tree_class)
            print(f'repository = {self.repozitory_name}\tnoom = {noom}')
            self.min_noom = min(noom, self.min_noom)
            self.max_noom = max(noom, self.max_noom)
            self.total_noom += 1
            self.noom += noom

            nocm = smethods_(tree_class)
            print(f'repository = {self.repozitory_name}\tnocm = {nocm}')
            self.min_nocm = min(nocm, self.min_nocm)
            self.max_nocm = max(nocm, self.max_nocm)
            self.total_nocm += 1
            self.nocm += nocm

            ncss = ncss_(raw)
            print(f'repository = {self.repozitory_name}\tncss = {ncss}')
            self.min_ncss = min(ncss, self.min_ncss)
            self.max_ncss = max(ncss, self.max_ncss)
            self.total_ncss += 1
            self.ncss += nooa

            noii = impls_(tree_class)
            print(f'repository = {self.repozitory_name}\tnoii = {noii}')
            self.min_noii = min(noii, self.min_noii)
            self.max_noii = max(noii, self.max_noii)
            self.total_noii += 1
            self.noii += noii

            napc = extnds_(tree_class)
            print(f'repository = {self.repozitory_name}\tnapc = {napc}')
            self.min_napc = min(napc, self.min_napc)
            self.max_napc = max(napc, self.max_napc)
            self.total_napc += 1
            self.napc += napc

            notp = gnrcs_(tree_class)
            print(f'repository = {self.repozitory_name}\tnotp = {notp}')
            self.min_notp = min(notp, self.min_notp)
            self.max_notp = max(notp, self.max_notp)
            self.total_notp += 1
            self.notp += notp

            final = final_(tree_class)
            print(f'repository = {self.repozitory_name}\tfinal = {final}')
            self.min_final = min(final, self.min_final)
            self.max_final = max(final, self.max_final)
            self.total_final += 1
            self.final += final

            noca = annts_(tree_class)
            print(f'repository = {self.repozitory_name}\tnoca = {noca}')
            self.min_noca = min(noca, self.min_noca)
            self.max_noca = max(noca, self.max_noca)
            self.total_noca += 1
            self.noca += noca

            varcomp = varcomp_(tree_class)
            print(f'repository = {self.repozitory_name}\tvarcomp = {varcomp}')
            self.min_varcomp = min(varcomp, self.min_varcomp)
            self.max_varcomp = max(varcomp, self.max_varcomp)
            self.total_varcomp += 1
            self.varcomp += varcomp

            mhf = mhf_(tree_class)
            print(f'repository = {self.repozitory_name}\tmhf = {self.mhf}')
            self.min_mhf = min(mhf, self.min_mhf)
            self.max_mhf = max(mhf, self.max_mhf)
            self.total_mhf += 1
            self.mhf += mhf

            smhf = smhf_(tree_class)
            print(f'repository = {self.repozitory_name}\tsmhf = {smhf}')
            self.min_smhf = min(smhf, self.min_smhf)
            self.max_smhf = max(smhf, self.max_smhf)
            self.total_smhf += 1
            self.smhf += smhf

            ahf = ahf_(tree_class)
            print(f'repository = {self.repozitory_name}\tahf = {ahf}')
            self.min_ahf = min(ahf, self.min_ahf)
            self.max_ahf = max(ahf, self.max_ahf)
            self.total_ahf += 1
            self.ahf += ahf

            sahf = sahf_(tree_class)
            print(f'repository = {self.repozitory_name}\tsahf = {sahf}')
            self.min_sahf = min(sahf, self.min_sahf)
            self.max_sahf = max(sahf, self.max_sahf)
            self.total_sahf += 1
            self.sahf += sahf

            nomp = nomp_(tree_class)
            print(f'repository = {self.repozitory_name}\tnomp = {nomp}')
            self.min_nomp = min(nomp, self.min_nomp)
            self.max_nomp = max(nomp, self.max_nomp)
            self.total_nomp += 1
            self.nomp += nomp

            nosmp = nosmp_(tree_class)
            print(f'repository = {self.repozitory_name}\tnosmp = {nosmp}')
            self.min_nosmp = min(nosmp, self.min_nosmp)
            self.max_nosmp = max(nosmp, self.max_nosmp)
            self.total_nosmp += 1
            self.nosmp += nosmp

            mxnomp = mxnomp_(tree_class)
            print(f'repository = {self.repozitory_name}\tmxnomp = {mxnomp}')
            self.min_mxnomp = min(mxnomp, self.min_mxnomp)
            self.max_mxnomp = max(mxnomp, self.max_mxnomp)
            self.total_mxnomp += 1
            self.mxnomp += mxnomp

            mxnosmp = mxnosmp_(tree_class)
            print(f'repository = {self.repozitory_name}\tmxnosmp = {mxnosmp}')
            self.min_mxnosmp = min(mxnosmp, self.min_mxnosmp)
            self.max_mxnosmp = max(mxnosmp, self.max_mxnosmp)
            self.total_mxnosmp += 1
            self.mxnosmp += mxnosmp

            nom = nom_(tree_class)
            print(f'repository = {self.repozitory_name}\tnom = {nom}')
            self.min_nom = min(nom, self.min_nom)
            self.max_nom = max(nom, self.max_nom)
            self.total_nom += 1
            self.nom += nom

            nop = nop_(tree_class)
            print(f'repository = {self.repozitory_name}\tnop = {nop}')
            self.min_nop = min(nop, self.min_nop)
            self.max_nop = max(nop, self.max_nop)
            self.total_nop += 1
            self.nop += nop

            nulls = nulls_(tree_class)
            print(f'repository = {self.repozitory_name}\tnulls = {nulls}')
            self.min_nulls = min(nulls, self.min_nulls)
            self.max_nulls = max(nulls, self.max_nulls)
            self.total_nulls += 1
            self.nulls += nulls

            doer = doer_(tree_class)
            print(f'repository = {self.repozitory_name}\tdoer = {doer}')
            self.min_doer = min(doer, self.min_doer)
            self.max_doer = max(doer, self.max_doer)
            self.total_doer += 1
            self.doer += doer

    def save_metrics(self):
        with open('files/java_metrics.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.repozitory_name,
                             self.min_nooa, self.max_nooa, self.aver_nooa,
                             self.min_nosa, self.max_nosa, self.aver_nosa,
                             self.min_nocc, self.max_nocc, self.aver_nocc,
                             self.min_noom, self.max_noom, self.aver_noom,
                             self.min_nocm, self.max_nocm, self.aver_nocm,
                             self.min_ncss, self.max_ncss, self.aver_ncss,
                             self.min_noii, self.max_noii, self.aver_noii,
                             self.min_napc, self.max_napc, self.aver_napc,
                             self.min_notp, self.max_notp, self.aver_notp,
                             self.min_final, self.max_final, self.aver_final,
                             self.min_noca, self.max_noca, self.aver_noca,
                             self.min_varcomp, self.max_varcomp, self.aver_varcomp,
                             self.min_mhf, self.max_mhf, self.aver_mhf,
                             self.min_smhf, self.max_smhf, self.aver_smhf,
                             self.min_ahf, self.max_ahf, self.aver_ahf,
                             self.min_sahf, self.max_sahf, self.aver_sahf,
                             self.min_nomp, self.max_nomp, self.aver_nomp,
                             self.min_nosmp, self.max_nosmp, self.aver_nosmp,
                             self.min_mxnomp, self.max_mxnomp, self.aver_mxnomp,
                             self.min_mxnosmp, self.max_mxnosmp, self.aver_mxnosmp,
                             self.min_nom, self.max_nom, self.aver_nom,
                             self.min_nop, self.max_nop, self.aver_nop,
                             self.min_nulls, self.max_nulls, self.aver_nulls,
                             self.min_doer, self.max_doer, self.aver_doer
                             ])
