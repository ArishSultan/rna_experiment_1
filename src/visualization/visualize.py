from matplotlib.pyplot import subplots, savefig
from sklearn.metrics import auc, RocCurveDisplay
from numpy import linspace, interp, mean, std, minimum, maximum


def generate_cv_auc(reports, filename):
    tprs = []
    aucs = []
    mean_fpr = linspace(0, 1, 100)
    fig, ax = subplots(figsize=(7.5, 7.5))

    for index, (y_true, y_pred) in enumerate(reports):
        viz = RocCurveDisplay.from_predictions(
            y_true,
            y_pred,
            name=f'ROC fold {index}',
            alpha=0.3,
            lw=1,
            ax=ax
        )

        interp_tpr = interp(mean_fpr, viz.fpr, viz.tpr)
        interp_tpr[0] = 0.0
        tprs.append(interp_tpr)
        aucs.append(viz.roc_auc)

    ax.plot([0, 1], [0, 1], "k--", label="chance level (AUC = 0.5)")
    mean_tpr = mean(tprs, axis=0)
    mean_tpr[-1] = 1.0
    mean_auc = auc(mean_fpr, mean_tpr)
    std_auc = std(aucs)
    ax.plot(
        mean_fpr,
        mean_tpr,
        color="b",
        label=r"Mean ROC (AUC = %0.2f $\pm$ %0.2f)" % (mean_auc, std_auc),
        lw=2,
        alpha=0.8,
    )

    std_tpr = std(tprs, axis=0)
    tprs_upper = minimum(mean_tpr + std_tpr, 1)
    tprs_lower = maximum(mean_tpr - std_tpr, 0)
    ax.fill_between(
        mean_fpr,
        tprs_lower,
        tprs_upper,
        color="grey",
        alpha=0.2,
        label=r"$\pm$ 1 std. dev.",
    )

    ax.set(
        xlim=[-0.05, 1.05],
        ylim=[-0.05, 1.05],
        xlabel="False Positive Rate",
        ylabel="True Positive Rate",
        title=f"Mean ROC curve with variability\n(Positive label')",
    )
    ax.axis("square")
    ax.legend(loc="lower right")
    savefig(f'reports/figures/{filename}.svg')

